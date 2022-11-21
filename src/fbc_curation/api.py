"""API for the frogrun web service.

This provides basic functionality of running the model
and returning the JSON representation based on fastAPI.
"""

import tempfile
import traceback
import typing
from pathlib import Path
from typing import Any, Dict, Optional

import orjson
import requests
import uvicorn
from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, FilePath
from pymetadata import log
from starlette.responses import FileResponse, JSONResponse

from fbc_curation import EXAMPLE_DIR
from fbc_curation.worker import frog_task


logger = log.get_logger(__name__)


class ORJSONResponse(JSONResponse):
    """JSON response."""

    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        """Render function."""
        content_bytes: bytes = orjson.dumps(content)
        return content_bytes


description = """
## 🐸 FROG webservice

This service provides an API for running FROG analysis.

After submission of a
model for frog analysis a `task_id` is returned which allows to query the status
of the FROG task and retrieve the FROG report after the task succeeded.
"""

api = FastAPI(
    default_response_class=ORJSONResponse,
    title="FROG REST API",
    description=description,
    version="0.2.0",
    terms_of_service="https://github.com/matthiaskoenig/fbc_curation/blob/develop/privacy_notice.md",  # noqa: E501
    contact={
        "name": "Matthias König",
        "url": "https://livermetabolism.com",
        "email": "konigmatt@googlemail.com",
        "orcid": "0000-0003-1725-179X",
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
            "name": "tasks",
            "description": "Task operations, such as querying status and "
            "retrieving results.",
        },
        {
            "name": "examples",
            "description": "FROG examples.",
        },
    ],
)


# API Permissions Data
origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/api")
def get_api_information(request: Request) -> Dict[str, Any]:
    """Get API information."""
    return {
        "title": api.title,
        "description": api.description,
        "contact": api.contact,
        "root_path": request.scope.get("root_path"),
    }


@api.get("/api/task/status/{task_id}", tags=["tasks"])
def get_status_for_task(task_id: str) -> JSONResponse:
    """Get status and results of FROG task with `task_id`."""
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return JSONResponse(result)


@api.get("/api/task/omex/{task_id}", tags=["tasks"])
async def get_combine_archive_for_task(task_id: str) -> FileResponse:
    """Get COMBINE archive (omex) for FROG task with `task_id`."""

    omex_path = Path("/frog_data") / f"FROG_{task_id}.omex"

    if not omex_path:
        raise HTTPException(
            status_code=404,
            detail=f"No COMBINE archive for task with " f"id '{task_id}'",
        )

    return FileResponse(
        path=omex_path, media_type="application/zip", filename=omex_path.name
    )


@api.post("/api/frog/file", tags=["frog"])
async def create_frog_from_file(request: Request) -> Dict[str, Any]:
    """Upload file and create FROG.

    Creates a task for the FROG report.

    :returns: `task_id`
    """
    file_data = await request.form()
    file_content = await file_data["source"].read()  # type: ignore
    return frog_from_bytes(file_content)


@api.post("/api/frog/content", tags=["frog"])
async def create_frog_from_content(request: Request) -> Dict[str, Any]:
    """Create FROG from file contents.

    Creates a task for the FROG report.

    :returns: `task_id`
    """
    content: bytes = await request.body()
    return frog_from_bytes(content)


@api.get("/api/frog/url", tags=["frog"])
def create_frog_from_url(url: str) -> Dict[str, Any]:
    """Create FROG via URL to SBML or COMBINE archive.

    Creates a task for the FROG report.

    :returns: `task_id`
    """
    response = requests.get(url)
    response.raise_for_status()
    return frog_from_bytes(response.content)


def frog_from_bytes(content: bytes) -> Dict[str, Any]:
    """Start FROG task for given content.

    Necessary to serialize the content to a common location
    accessible for the task queue.

    :returns: `task_id`
    """
    try:
        # persistent temporary file cleaned up by task
        _, path = tempfile.mkstemp(dir="/frog_data")

        with open(path, "w+b") as f_tmp:
            f_tmp.write(content)
            f_tmp.close()
        task = frog_task.delay(str(path))
        return {"task_id": task.id}

    except Exception as e:
        res = {
            "errors": [
                f"{e.__str__()}",
                f"{''.join(traceback.format_exception(None, e, e.__traceback__))}",
            ],
        }
        logger.error(res)

        return res


class Example(BaseModel):
    """Metadata for example model on sbml4humans."""

    id: str
    file: FilePath
    description: Optional[str] = None


_example_items: Dict[str, Example] = {
    "e_coli_core_sbml": Example(
        id="e_coli_core_sbml",
        file=EXAMPLE_DIR / "models" / "e_coli_core.xml",
        description="E.coli core model from BiGG database as SBML.",
    ),
    "e_coli_core_omex": Example(
        id="e_coli_core_omex",
        file=EXAMPLE_DIR / "models" / "e_coli_core.omex",
        description="E.coli core model from BiGG database as OMEX.",
    ),
    "iJR904": Example(
        id="iJR904",
        file=EXAMPLE_DIR / "models" / "iJR904.omex",
        description="iJR904 model from BiGG database as OMEX.",
    ),
}
examples = [example.dict() for example in _example_items.values()]


@api.get("/api/examples", tags=["examples"])
def get_examples() -> Dict[Any, Any]:
    """Get FROG examples."""
    return {"examples": examples}


@api.get("/api/examples/{example_id}", tags=["examples"])
def create_frog_for_example(example_id: str) -> Dict[str, Any]:
    """Get specific FROG example.

    Creates a task for the FROG report.

    :returns: task_id
    """

    example: Optional[Example] = _example_items.get(example_id, None)
    if example:
        source: Path = example.file
        with open(source, "rb") as f:
            content: bytes = f.read()
            return frog_from_bytes(content)

    else:
        return {"error": f"Example for id '{example_id}' does not exist."}


if __name__ == "__main__":
    # http://localhost:1555/
    # http://localhost:1555/docs

    uvicorn.run(
        "fbc_curation.api:api",
        host="localhost",
        port=1555,
        log_level="info",
        reload=True,
    )
