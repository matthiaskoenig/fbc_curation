"""Testing worker."""

from pathlib import Path

from fbc_curation import EXAMPLE_DIR
from fbc_curation.worker import frog_task


model_path: Path = EXAMPLE_DIR / "models" / "e_coli_core.xml"


def test_frog_task(tmp_path: Path) -> None:
    """Test execution of frog task."""
    omex_path: Path = tmp_path / "test.omex"
    content = frog_task(source_path_str=str(model_path), omex_path_str=str(omex_path))
    assert content
