"""Configuration for pytest."""
from typing import Dict

import pytest


@pytest.fixture(scope="session")
def celery_config() -> Dict[str, str]:
    """Celery configuration fixture."""
    return {"broker_url": "amqp://", "result_backend": "redis://"}
