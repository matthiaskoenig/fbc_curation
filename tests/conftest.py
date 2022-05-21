"""Configuration for pytest."""
from pathlib import Path
from typing import Dict

import pytest

from fbc_curation import EXAMPLE_DIR


@pytest.fixture(scope="session")
def celery_config() -> Dict[str, str]:
    """Celery configuration fixture."""
    return {"broker_url": "amqp://", "result_backend": "redis://"}


@pytest.fixture
def ecoli_sbml_path() -> Path:
    """Path to Ecoli core SBML model."""
    return EXAMPLE_DIR / "models" / "e_coli_core.xml"
