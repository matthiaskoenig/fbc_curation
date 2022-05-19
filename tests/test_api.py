"""Test API functionality."""

from fastapi.testclient import TestClient

from fbc_curation.api import api


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
