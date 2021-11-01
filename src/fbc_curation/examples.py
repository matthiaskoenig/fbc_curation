"""Create curation information for example models."""
from pathlib import Path

from pymetadata import log

from fbc_curation import EXAMPLE_PATH
from fbc_curation.compare import Comparison
from fbc_curation.worker import frog_task


logger = log.get_logger(__name__)


def run_examples() -> None:
    """Run all examples."""
    example_ecoli_core()
    example_ecoli_core_omex()
    example_iJR904()
    example_iJR904_omex()
    example_iCGB21FR()


def example_ecoli_core() -> None:
    """Create FROG report for ecoli core."""
    return _run_example(
        EXAMPLE_PATH / "models" / "e_coli_core.xml",
        EXAMPLE_PATH / "frogs" / "e_coli_core_FROG.xml",
    )


def example_ecoli_core_no_genes() -> None:
    """Create FROG report for ecoli core."""
    return _run_example(
        EXAMPLE_PATH / "models" / "e_coli_core_no_genes.xml",
        EXAMPLE_PATH / "frogs" / "e_coli_core_no_genes_FROG.xml",
    )


def example_ecoli_core_omex() -> None:
    """Create FROG report for ecoli core."""
    return _run_example(
        EXAMPLE_PATH / "models" / "e_coli_core.omex",
        EXAMPLE_PATH / "models" / "e_coli_core_omex_FROG.omex",
    )


def example_iJR904() -> None:
    """Create FROG report for iJR904."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iJR904.xml",
        EXAMPLE_PATH / "frogs" / "iJR904_FROG.xml",
    )


def example_iJR904_omex() -> None:
    """Create FROG report for iJR904."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iJR904.omex",
        EXAMPLE_PATH / "frogs" / "iJR904_omex_FROG.omex",
    )


def example_iCGB21FR() -> None:
    """Create FROG report for iCGB21FR."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iCGB21FR.omex",
        EXAMPLE_PATH / "frogs" / "iCGB21FR_FROG.omex",
    )


def example_iAB_AMO1410_SARS_omex() -> None:
    """Create FROG report for iAB_AMO1410_SARS."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iAB_AMO1410_SARS-CoV-2.omex",
        EXAMPLE_PATH / "frogs" / "iAB_AMO1410_SARS-CoV-2_omex_FROG.omex",
    )


def _run_example(model_path: Path, omex_path: Path) -> None:
    """Run single example helper function."""
    frog_task(
        source_path_str=str(model_path),
        input_is_temporary=False,
        omex_path_str=str(omex_path),
    )
    model_reports = Comparison.read_reports_from_omex(omex_path=omex_path)
    for model_location, reports in model_reports.items():
        Comparison.compare(location=model_location, reports=reports)


if __name__ == "__main__":
    # run_examples()
    example_iCGB21FR()
    # example_ecoli_core_no_genes()
