"""Create curation information for example models."""
from pathlib import Path

from pymetadata import log
from pymetadata.console import console
from pymetadata.omex import EntryFormat, ManifestEntry, Omex

from fbc_curation import EXAMPLE_DIR
from fbc_curation.compare import FrogComparison
from fbc_curation.worker import run_frog


logger = log.get_logger(__name__)

example_models = [
    "e_coli_core.xml",
    "e_coli_core_no_genes.xml",
    "e_coli_core.omex",
    "iJR904.xml",
    "iJR904.omex",
    "iCGB21FR.omex",
]


def create_omex_for_models() -> None:
    """Create omex files for models."""
    for example in ["e_coli_core.xml", "iJR904.xml"]:
        model_path: Path = EXAMPLE_DIR / "models" / example
        omex = Omex()
        omex.add_entry(
            entry_path=model_path,
            entry=ManifestEntry(
                location=f"./{example}", format=EntryFormat.SBML, master=True
            ),
        )
        omex_path = model_path.parent / f"{model_path.stem}.omex"
        console.log(omex_path)
        omex.to_omex(omex_path=omex_path)


def run_examples() -> None:
    """Run all examples."""
    for model_filename in example_models:
        run_example(model_filename)


def run_example(filename: str) -> Path:
    """Run single example helper function."""

    model_path = EXAMPLE_DIR / "models" / filename
    omex_path = EXAMPLE_DIR / "frogs" / f"{filename.split('.')[0]}_FROG.omex"

    run_frog(
        source_path=model_path,
        omex_path=omex_path,
    )
    model_reports = FrogComparison.read_reports_from_omex(omex_path=omex_path)
    for _, reports in model_reports.items():
        FrogComparison.compare_reports(reports=reports)

    return omex_path


if __name__ == "__main__":
    # create_omex_for_models()
    run_examples()
