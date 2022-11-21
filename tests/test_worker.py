"""Testing worker."""

from pathlib import Path

from fbc_curation.worker import frog_task


def test_frog_task(tmp_path: Path, ecoli_sbml_path: Path) -> None:
    """Test execution of frog task."""
    omex_path: Path = tmp_path / "test.omex"
    content = frog_task(
        source_path_str=str(ecoli_sbml_path), omex_path_str=str(omex_path)
    )
    assert content
