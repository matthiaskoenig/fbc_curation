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

from fbc_curation.worker import create_task, frog_task
from fbc_curation import EXAMPLE_PATH

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

'''
Development
http://localhost:8085/
curl http://localhost:1556/api/tasks/ -H "Content-Type: application/json" --data '{"type": 1}'
curl http://localhost:1556/api/tasks/d5404acb-c576-45df-a661-bbbeae2260f1
docker container logs --follow frog_worker

'''


class TaskInfo(BaseModel):
    type: int


@api.post("/api/tasks/", status_code=201)
def run_task(info: TaskInfo):
    task = create_task.delay(info.type)
    return JSONResponse({"task_id": task.id})


@api.get("/api/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


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

            task = frog_task.delay(str(path))
            return {"task_id": task.id}

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

            task = frog_task.delay(str(path))
            return {"task_id": task.id}

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

            task = frog_task.delay(str(path))
            return {"task_id": task.id}

    except Exception as e:
        return _handle_error(e, info={})


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
            task = frog_task.delay(str(source))
            return {"task_id": task.id}
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
