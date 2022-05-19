"""Test runfrog command line scripts and options."""

import sys
from pathlib import Path
from typing import Any

import pytest

from fbc_curation import EXAMPLE_DIR, runfrog


@pytest.mark.parametrize("filename", ["e_coli_core.xml", "e_coli_core.omex"])
def test_runfrog1(monkeypatch: Any, tmp_path: Path, filename: str) -> None:
    """First example via command line tool.

    runfrog --input resources/examples/models/e_coli_core.xml
    --output resources/examples/results/e_coli_core.omex
    """
    output_path = tmp_path / "test.omex"
    with monkeypatch.context() as m:
        args = [
            "runfrog",
            "--input",
            f"{EXAMPLE_DIR / 'models' / filename}",
            "--output",
            output_path,
        ]
        m.setattr(sys, "argv", args)
        runfrog.main()

        assert output_path.exists()


@pytest.mark.skip(reason="Comparison to reference files not implemented.")
def test_runfrog2(monkeypatch: Any, tmp_path: Path) -> None:
    """Second example via command line tool.

    runfrog --input resources/examples/models/e_coli_core.xml
    --output resources/examples/results/e_coli_core.omex
    --reference resources/examples/results/e_coli_core/cobrapy
    """
    output_path = tmp_path / "test.omex"
    with monkeypatch.context() as m:
        args = [
            "runfrog",
            "--input",
            f"{EXAMPLE_DIR / 'models' / 'e_coli_core.xml'}",
            "--output",
            output_path,
            "--reference",
            f"{EXAMPLE_DIR / 'results' / 'e_coli_core' / 'e_coli_core_FROG'}",
        ]
        m.setattr(sys, "argv", args)
        runfrog.main()

        assert output_path.exists()
