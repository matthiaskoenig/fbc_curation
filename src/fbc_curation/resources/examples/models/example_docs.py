"""FROG example using `fbc_curation`."""
from pathlib import Path

from fbc_curation.compare import FrogComparison
from fbc_curation.worker import run_frog


def create_frog(model_path: Path, omex_path: Path) -> None:
    """Create FROG report and writes OMEX for given model."""

    # create FROG and write to COMBINE archive
    run_frog(
        source_path=model_path,
        omex_path=omex_path,
    )

    # compare FROG results in created COMBINE archive
    model_reports = FrogComparison.read_reports_from_omex(omex_path=omex_path)
    for _, reports in model_reports.items():
        FrogComparison.compare_reports(reports=reports)


if __name__ == "__main__":
    base_path = Path(".")
    create_frog(
        model_path=base_path / "e_coli_core.xml",
        omex_path=base_path / "e_coli_core_FROG.omex",
    )
