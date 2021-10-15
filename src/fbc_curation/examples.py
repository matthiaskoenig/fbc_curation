"""Create curation information for example models."""
from pathlib import Path
from typing import Dict

from pymetadata.console import console

from fbc_curation import EXAMPLE_PATH
from fbc_curation.curator import Curator, FROGResults
from fbc_curation.curator.cameo_curator import CuratorCameo
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy


def run_examples(results_path: Path = EXAMPLE_PATH / "results"):
    """Run all examples."""
    example_ecoli_core(results_path=results_path / "e_coli_core")
    example_iJR904(results_path=results_path / "iJR904")
    example_iAB_AMO1410_SARS(results_path=results_path / "iAB_AMO1410_SARS")


def example_ecoli_core(results_path: Path) -> Dict:
    """Create example files for ecoli core."""
    return _run_example(
        EXAMPLE_PATH / "models" / "e_coli_core.xml", results_path=results_path
    )


def example_iJR904(results_path: Path) -> Dict:
    """Create example files for iJR904."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iJR904.xml.gz", results_path=results_path
    )


def example_iAB_AMO1410_SARS(results_path: Path) -> Dict:
    """Create example files for iAB_AMO1410_SARS."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iAB_AMO1410_SARS-CoV-2.xml",
        results_path=results_path,
    )


def _run_example(model_path: Path, results_path: Path) -> Dict:
    console.rule(str(model_path))
    obj_info = Curator.read_objective_information(model_path)

    curator_keys = ["cobrapy", "cameo"]
    for k, curator_class in enumerate([CuratorCobrapy, CuratorCameo]):
        curator = curator_class(
            model_path=model_path, objective_id=obj_info.active_objective
        )
        results: FROGResults = curator.run()
        results.write_results(results_path / curator_keys[k])

    all_results = {}
    for curator_key in curator_keys:
        all_results[curator_key] = FROGResults.read_results(
            path_in=results_path / curator_key
        )

    # comparison
    valid = [r.validate() for r in all_results.values()]
    equal = FROGResults.compare(all_results)
    info = {
        "model_path": model_path,
        "valid": valid,
        "equal": equal,
    }
    console.print(info)
    return info


if __name__ == "__main__":
    # run_examples()
    example_ecoli_core(results_path=EXAMPLE_PATH / "results" / "e_coli_core")
