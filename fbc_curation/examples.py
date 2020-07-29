"""
Create curation information for example models.
"""
from pathlib import Path
from fbc_curation import EXAMPLE_PATH
from fbc_curation.curator import Curator, CuratorResults
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
from fbc_curation.curator.cameo_curator import CuratorCameo


def run_examples(results_path=EXAMPLE_PATH / "results"):
    example_ecoli_core(results_path=results_path / "e_coli_core")
    example_iJR904(results_path=results_path / "iJR904")
    example_iAB_AMO1410_SARS(results_path=results_path / "iAB_AMO1410_SARS")


def example_ecoli_core(results_path):
    """Create example files for ecoli core."""
    _run_example(EXAMPLE_PATH / "models" / "e_coli_core.xml", results_path=results_path)


def example_iJR904(results_path):
    """Create example files for ecoli core."""
    _run_example(EXAMPLE_PATH / "models" / "iJR904.xml.gz", results_path=results_path)


def example_iAB_AMO1410_SARS(results_path):
    _run_example(EXAMPLE_PATH / "models" / "iAB_AMO1410_SARS-CoV-2.xml", results_path=results_path)


def _run_example(model_path: Path, results_path: Path) -> None:
    print("#" * 80)
    print(model_path)
    print("#" * 80)
    obj_info = Curator.read_objective_information(model_path)

    curator_keys = ["cobrapy", "cameo"]
    for k, curator_class in enumerate([CuratorCobrapy, CuratorCameo]):
        curator = curator_class(model_path=model_path, objective_id=obj_info.active_objective)
        results = curator.run()  # type: CuratorResults
        results.write_results(results_path / curator_keys[k])

    all_results = {}
    for curator_key in curator_keys:
        all_results[curator_key] = CuratorResults.read_results(path_in=results_path / curator_key)

    # comparison
    CuratorResults.compare(all_results)


if __name__ == "__main__":
    # run_examples()
    example_ecoli_core(results_path=EXAMPLE_PATH / "results" / "e_coli_core")
    # example_iAB_AMO1410_SARS(results_path=EXAMPLE_PATH / "results" / "iAB_AMO1410_SARS")
