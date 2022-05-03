"""Create curation information for example models."""
from pathlib import Path

from pymetadata.console import console
from pymetadata.omex import EntryFormat, ManifestEntry, Omex
from pymetadata import log

from fbc_curation import EXAMPLE_DIR
from fbc_curation.compare import Comparison
from fbc_curation.worker import frog_task


logger = log.get_logger(__name__)

example_models = [
    "e_coli_core.xml",
    "e_coli_core_no_genes.xml",
    "e_coli_core.omex",
    "iJR904.xml",
    "iJR904.omex",
    "iCGB21FR.omex"
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
        _run_example(model_filename)


def _run_example(filename: str) -> Path:
    """Run single example helper function."""

    model_path = EXAMPLE_DIR / "models" / filename
    omex_path = EXAMPLE_DIR / "frogs" / f"{filename.split('.')[0]}_FROG.omex"

    frog_task(
        source_path_str=str(model_path),
        input_is_temporary=False,
        omex_path_str=str(omex_path),
    )
    model_reports = Comparison.read_reports_from_omex(omex_path=omex_path)
    for model_location, reports in model_reports.items():
        Comparison.compare(location=model_location, reports=reports)

    return omex_path


if __name__ == "__main__":
    create_omex_for_models()
    run_examples()

