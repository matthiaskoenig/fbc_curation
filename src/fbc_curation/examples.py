"""Create curation information for example models."""
from pathlib import Path
from typing import Dict

from pymetadata.console import console
from pymetadata.omex import EntryFormat, ManifestEntry, Omex

from fbc_curation import EXAMPLE_PATH
from fbc_curation.curator import Curator
from fbc_curation.curator.cameo_curator import CuratorCameo
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
from fbc_curation.frog import CuratorConstants, FrogReport
from fbc_curation.worker import frog_task


def run_examples(results_path: Path = EXAMPLE_PATH / "results") -> None:
    """Run all examples."""
    example_ecoli_core(results_path=results_path / "e_coli_core")
    example_iJR904(results_path=results_path / "iJR904")
    example_iAB_AMO1410_SARS(results_path=results_path / "iAB_AMO1410_SARS")


def example_ecoli_core(results_path: Path) -> Dict:
    """Create FROG report for ecoli core."""
    return _run_example(
        EXAMPLE_PATH / "models" / "e_coli_core.xml", results_path=results_path
    )


def example_ecoli_core_omex(results_path: Path) -> Dict:
    """Create FROG report for ecoli core."""
    return _run_example(
        EXAMPLE_PATH / "models" / "e_coli_core.omex", results_path=results_path
    )


def example_iJR904(results_path: Path) -> Dict:
    """Create FROG report for iJR904."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iJR904.xml", results_path=results_path
    )


def example_iJR904_omex(results_path: Path) -> Dict:
    """Create FROG report for iJR904."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iJR904.omex", results_path=results_path
    )


def example_iAB_AMO1410_SARS(results_path: Path) -> Dict:
    """Create FROG report for iAB_AMO1410_SARS."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iAB_AMO1410_SARS-CoV-2.xml",
        results_path=results_path,
    )


def example_iAB_AMO1410_SARS_omex(results_path: Path) -> Dict:
    """Create FROG report for iAB_AMO1410_SARS."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iAB_AMO1410_SARS-CoV-2.omex",
        results_path=results_path,
    )


def _run_example(model_path: Path, results_path: Path) -> Dict:
    """Run single example helper function."""

    omex_path = results_path / f"{model_path.stem}_FROG.omex"
    frog_task(
        source_path_str=str(model_path),
        input_is_temporary=False,
        omex_path_str=str(omex_path),
    )

    # FIXME: reading and comparison
    # Read all reports
    # all_results: Dict[str: FrogReport] = {}
    # for curator_key in curator_keys:
    #     all_results[curator_key] = FrogReport.read_json(
    #         path=results_path / curator_key / CuratorConstants.REPORT_FILENAME
    #     )

    # comparison
    info: Dict = {}
    # valid = [r.validate() for r in all_results.values()]
    # equal = FrogReport.compare(all_results)
    # info = {
    #     "model_path": model_path,
    #     "valid": valid,
    #     "equal": equal,
    # }
    # console.print(info)
    return info


if __name__ == "__main__":
    # run_examples()
    example_ecoli_core(results_path=EXAMPLE_PATH / "results" / "e_coli_core")
    # TODO: comparison
    # TODO: second curator
