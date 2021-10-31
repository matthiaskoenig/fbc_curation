"""Create curation information for example models."""
from pathlib import Path
from typing import Dict, List

import orjson
from pymetadata import log
from pymetadata.console import console
from pymetadata.omex import EntryFormat, ManifestEntry, Omex

from fbc_curation import EXAMPLE_PATH
from fbc_curation.curator import Curator
from fbc_curation.curator.cameo_curator import CuratorCameo
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
from fbc_curation.frog import CuratorConstants, FrogReport
from fbc_curation.worker import frog_task


logger = log.get_logger(__name__)


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

    # Read all reports from JSON (FIXME: support reading from TSV)
    reports: List[FrogReport] = []
    omex = Omex.from_omex(omex_path)
    for entry in omex.manifest.entries:
        if entry.format == EntryFormat.FROG_JSON_V1:
            report = FrogReport.from_json(path=omex.get_path(entry.location))
            reports.append(report)
        elif entry.format == EntryFormat.FROG_METADATA_V1:
            path = omex.get_path(entry.location).parent
            report = FrogReport.from_tsv(path)
            reports.append(report)

    # get model reports per model
    model_reports = Dict[str, Dict[str, FrogReport]]
    for report in model_reports:
        model_location = report.metadata.model_location
        d = model_reports.get(model_location, {})
        frog_id = report.metadata.frog_id
        if frog_id in d:
            logger.error(f"duplicate FROG report: '{frog_id}' for '{model_path}'")
        d[frog_id] = report
        model_reports[model_location] = d

    for location, reports_dict in model_reports.items():
        logger.info(f"{location}: {reports_dict.keys()}")

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
