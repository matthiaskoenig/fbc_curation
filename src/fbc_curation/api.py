"""API for the frogrun web service.

This provides basic functionality of running the model
and returning the JSON representation based on fastAPI.
"""

import tempfile
import time
import traceback
import uuid
from pathlib import Path
from typing import Any, Dict, Optional, Union

import libsbml
import requests
import uvicorn
from fastapi import FastAPI, Request, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, FilePath
from pymetadata import log
from pymetadata.console import console
from pymetadata.omex import EntryFormat, Manifest, ManifestEntry, Omex
from starlette.responses import JSONResponse

from fbc_curation.worker import create_task
from fbc_curation import EXAMPLE_PATH
from fbc_curation.curator import Curator
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
from fbc_curation.frog import FrogReport

logger = log.get_logger(__name__)

api = FastAPI(
    title="FROG REST API",
    description="API for running FROG analysis",
    version="0.1.0",
    terms_of_service="https://github.com/matthiaskoenig/fbc_curation/blob/develop/privacy_notice.md",
    contact={
        "name": "Matthias König",
        "url": "https://livermetabolism.com",
        "email": "konigmatt@googlemail.com",
    },
    license_info={
        "name": "LGPLv3",
        "url": "http://opensource.org/licenses/LGPL-3.0",
    },
    openapi_tags=[
        {
            "name": "frog",
            "description": "Create FROG report.",
        },
        {
            "name": "examples",
            "description": "Manage and query examples.",
        },
    ],
)


# API Permissions Data
origins = [
    # "localhost",
    # "localhost:3456",
    # "sbml4humans.de",
    "*"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Example(BaseModel):
    """Metadata for example model on sbml4humans."""

    id: str
    file: FilePath
    description: Optional[str] = None


example_items: Dict[str, Example] = {
    "e_coli_core": Example(
        id="e_coli_core",
        file=EXAMPLE_PATH / "models" / "e_coli_core.xml",
        description="E.coli core model from BiGG database.",
    ),
    "iAB_AMO1410_SARS-CoV-2": Example(
        id="iAB_AMO1410_SARS-CoV-2",
        file=EXAMPLE_PATH / "models" / "iAB_AMO1410_SARS-CoV-2.xml",
        description="iAB_AMO1410_SARS-CoV-2 model.",
    ),
    "iJR904": Example(
        id="iJR904",
        file=EXAMPLE_PATH / "models" / "iJR904.xml.gz",
        description="iJR904 model from BiGG database.",
    ),
}


@api.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@api.get("/api/url", tags=["frog"])
def frog_from_url(url: str) -> Dict[Any, Any]:
    """Get JSON FROG via URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        with tempfile.TemporaryDirectory() as f_tmp:
            path = Path(f_tmp) / "file"
            with open(path, "w") as f:
                f.write(response.text)

            return json_for_omex(path)

    except Exception as e:
        return _handle_error(e, info={"url": url})


@api.post("/api/file", tags=["frog"])
async def frog_from_file(request: Request) -> Dict[Any, Any]:
    """Upload file and return JSON FROG."""
    try:
        file_data = await request.form()
        file_content = await file_data["source"].read()  # type: ignore

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "file"
            with open(path) as f:
                f.write(file_content)

            return json_for_omex(path)

    except Exception as e:
        return _handle_error(e, info={})


@api.post("/api/content", tags=["frog"])
async def frog_from_content(request: Request) -> Dict[Any, Any]:
    """Get JSON FROG from file contents."""

    file_content: Optional[str]
    try:
        file_content_bytes: bytes = await request.body()
        file_content = file_content_bytes.decode("utf-8")

        # FIXME: get/use name
        with tempfile.TemporaryDirectory() as f_tmp:
            path = Path(f_tmp) / "file"
            with open(path, "w") as f:
                f.write(file_content)

            return json_for_omex(path)

    except Exception as e:
        return _handle_error(e, info={})


def json_for_omex(omex_path: Path) -> Dict[str, Any]:
    """Create FROG JSON for omex path.

    Path can be either Omex or an SBML file.
    """
    uid: str = uuid.uuid4().hex

    if Omex.is_omex(omex_path):
        omex = Omex().from_omex(omex_path)
    else:
        # Path is SBML we create a new archive
        omex = Omex()
        omex.add_entry(
            entry_path=omex_path,
            entry=ManifestEntry(
                location="./model.xml", format=EntryFormat.SBML, master=True
            ),
        )

    content = {"uid": uid, "manifest": omex.manifest.dict(), "frogs": {}}

    # Add FROG JSON for all SBML files
    entry: ManifestEntry
    for entry in omex.manifest.entries:
        if entry.is_sbml():
            sbml_path: Path = omex.get_path(entry.location)
            content["frogs"][entry.location] = json_for_sbml(  # type: ignore
                uid=uid, source=sbml_path
            )

    return content


def json_for_sbml(uid: str, source: Union[Path, str, bytes]) -> Dict:
    """Create FROG JSON content for given SBML source.

    Source is either path to SBML file or SBML string.
    """

    if isinstance(source, bytes):
        source = source.decode("utf-8")

    time_start = time.time()
    frog_json = frog_json_for_sbml(source=source)
    time_elapsed = round(time.time() - time_start, 3)

    debug = False
    if debug:
        console.rule("Creating JSON FROG")
        console.print(frog_json)
        console.rule()

    logger.info(f"JSON created for '{uid}' in '{time_elapsed}'")

    return frog_json


def frog_json_for_sbml(source: Union[Path, str]) -> Dict:
    """Read model info from SBML."""

    with tempfile.TemporaryDirectory() as f_tmp:
        if isinstance(source, Path):
            sbml_path = source
        elif isinstance(source, str):
            sbml_path = Path(f_tmp) / "model.sbml"
            with open(sbml_path, "w") as f_sbml:
                f_sbml.write(source)

        # return SBMLDocumentInfo(doc=doc)
        # curator_keys = ["cobrapy", "cameo"]
        obj_info = Curator._read_objective_information(sbml_path)
        curator = CuratorCobrapy(
                model_path=sbml_path, objective_id=obj_info.active_objective
        )
        report: FrogReport = curator.run()
        return report


def _handle_error(e: Exception, info: Optional[Dict] = None) -> Dict[Any, Any]:
    """Handle exceptions in the backend.

    All calls are wrapped in a try/except which will provide the errors to the frontend.

    :param info: optional dictionary with information.
    """

    res = {
        "errors": [
            f"{e.__str__()}",
            f"{''.join(traceback.format_exception(None, e, e.__traceback__))}",
        ],
        "warnings": [],
        "info": info,
    }
    logger.error(res)

    return res


@api.get("/api/examples", tags=["examples"])
def examples() -> Dict[Any, Any]:
    """Get FROG examples."""
    try:
        example: Example
        return {"examples": [example.dict() for example in example_items.values()]}

    except Exception as e:
        return _handle_error(e)


@api.get("/api/examples/{example_id}", tags=["examples"])
def example(example_id: str) -> Dict[Any, Any]:
    """Get specific FROG example."""
    try:
        example: Optional[Example] = example_items.get(example_id, None)
        content: Dict
        if example:
            source: Path = example.file  # type: ignore
            content = json_for_omex(omex_path=source)
        else:
            content = {"error": f"example for id does not exist '{example_id}'"}

        return content
    except Exception as e:
        return _handle_error(e)


if __name__ == "__main__":
    # http://localhost:1555/api
    # http://localhost:1555/api/docs

    uvicorn.run(
        "fbc_curation.api:api",
        host="localhost",
        port=1555,
        log_level="info",
        reload=True,
    )
