"""Test API functionality."""
from pathlib import Path

from starlette.responses import JSONResponse
from fastapi.testclient import TestClient

from fbc_curation.api import api
from fbc_curation.frog import FrogReport
from fbc_curation.worker import run_frog, _frog_for_sbml

client = TestClient(api)


def test_get_api_information() -> None:
    """Test /api endpoint."""
    response = client.get("/api")
    assert response.status_code == 200
    json = response.json()
    assert json
    for key in [
        "title",
        "description",
        "contact",
        "root_path",
    ]:
        assert key in json


def test_get_examples() -> None:
    """Test /api/examples endpoint."""
    response = client.get("/api/examples")
    assert response.status_code == 200
    json = response.json()
    assert json
    for key in [
        "examples",
    ]:
        assert key in json


def test_json_for_ecoli_frog(ecoli_sbml_path: Path) -> None:
    """Test JSON serialization of results."""
    report: FrogReport = _frog_for_sbml(
        source=ecoli_sbml_path, curator_key="cobrapy"
    )
    response = JSONResponse(report.dict())
    assert response
