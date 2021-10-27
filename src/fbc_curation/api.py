"""API for the frogrun web service.

This provides basic functionality of running the model
and returning the JSON representation based on fastAPI.
"""

import tempfile
import time
import traceback
import typing
import uuid
from pathlib import Path
from typing import Any, Dict, Optional, Union

import libsbml
import requests
import uvicorn
import orjson
from celery.result import AsyncResult

from fastapi import FastAPI, Request, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, FilePath
from pymetadata import log
from starlette.responses import JSONResponse

from fbc_curation.worker import frog_task
from fbc_curation import EXAMPLE_PATH
from fbc_curation import FROG_DATA_DIR

logger = log.get_logger(__name__)


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content)


api = FastAPI(
    default_response_class=ORJSONResponse,
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
        {
            "name": "tasks",
            "description": "Task queue operations.",
        },
    ],
)


# API Permissions Data
origins = [
    "*"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/api/tasks/{task_id}", tags=["task"])
def get_status(task_id: str) -> JSONResponse:
    """Status and results of task for id."""
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


@api.get("/api/url", tags=["frog"])
def frog_from_url(url: str) -> Dict[str, Any]:
    """Create FROG via URL.

    Creates a task for the FROG report.
    :returns: task_id
    """
    response = requests.get(url)
    response.raise_for_status()
    return frog_from_bytes(response.content)


@api.post("/api/file", tags=["frog"])
async def frog_from_file(request: Request) -> Dict[str, Any]:
    """Upload file and create FROG.

    Creates a task for the FROG report.
    :returns: task_id
    """
    file_data = await request.form()
    file_content = await file_data["source"].read()  # type: ignore
    return frog_from_bytes(file_content)


@api.post("/api/content", tags=["frog"])
async def frog_from_content(request: Request) -> Dict[str, Any]:
    """Create FROG from file contents.

    Creates a task for the FROG report.
    :returns: task_id
    """
    content: bytes = await request.body()
    return frog_from_bytes(content)


def frog_from_bytes(content: bytes) -> Dict[str, Any]:
    """Start FROG task for given content.

    Necessary to serialize the content to a common location
    accessible for the task queue.
    :returns: task_id
    """
    # FIXME: This is currently not working correctly
    try:
        # persistent temporary file cleaned up by task
        _, path = tempfile.mkstemp(dir="/frog_data")

        with open(path, "wb") as f_tmp:
            logger.warning(content)
            f_tmp.write(content)
        logger.error(f"Saving content in: {str(path)}")
        task = frog_task.delay(str(path), True)
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
        file=EXAMPLE_PATH / "models" / "e_coli_core.xml",
        description="E.coli core model from BiGG database as SBML.",
    ),
    "e_coli_core_omex": Example(
        id="e_coli_core_omex",
        file=EXAMPLE_PATH / "models" / "e_coli_core.omex",
        description="E.coli core model from BiGG database as OMEX.",
    ),
    "iAB_AMO1410_SARS-CoV-2": Example(
        id="iAB_AMO1410_SARS-CoV-2",
        file=EXAMPLE_PATH / "models" / "iAB_AMO1410_SARS-CoV-2.omex",
        description="iAB_AMO1410_SARS-CoV-2 model as OMEX.",
    ),
    "iJR904": Example(
        id="iJR904",
        file=EXAMPLE_PATH / "models" / "iJR904.omex",
        description="iJR904 model from BiGG database as OMEX.",
    ),
}
examples = [example.dict() for example in _example_items.values()]


@api.get("/api/examples", tags=["examples"])
def examples() -> Dict[Any, Any]:
    """Get FROG examples."""
    return {
        "examples": examples
    }


@api.get("/api/examples/{example_id}", tags=["examples"])
def example(example_id: str) -> Dict[str, Any]:
    """Get specific FROG example.

    Creates a task for the FROG report.
    :returns: task_id
    """

    example: Optional[Example] = _example_items.get(example_id, None)
    content: Dict
    if example:
        source: Path = example.file  # type: ignore
        with open(source, "rb") as f:
            content = f.read()
            return frog_from_bytes(content)

    else:
        return {
            "error": f"Example for id '{example_id}' does not exist."
        }


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
