"""
Create curation information for example models.
"""
from pathlib import path
from fbc_curation import EXAMPLE_PATH
from fbc_curation.curator.result import CuratorResult
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
from fbc_curation.curator.cameo_curator import CuratorCameo


def _run_example(model_path: Path, results_path: Path)

def example_ecoli_core(results_path):
    """Create example files for ecoli core."""
    model_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"
    creator = FBCFileCreator(model_path=model_path, results_path=results_path)
    creator.create_fbc_files()


def example_iJR904(results_path):
    """Create example files for ecoli core."""
    model_path = EXAMPLE_PATH / "models" / "iJR904.xml.gz"
    creator = FBCFileCreator(model_path=model_path, results_path=results_path)
    creator.create_fbc_files()


def example_MODEL1709260000(results_path):
    """Create example files for MODEL1709260000."""
    model_path = EXAMPLE_PATH / "models" / "MODEL1709260000.xml.gz"
    creator = FBCFileCreator(model_path=model_path, results_path=results_path)
    creator.create_fbc_files()


def run_examples(results_path=EXAMPLE_PATH / "results"):
    example_ecoli_core(results_path / "e_coli_core")
    example_iJR904(results_path / "iJR904")
    example_MODEL1709260000(results_path / "MODEL1709260000")


if __name__ == "__main__":
    # run_examples()


    model_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"
    results_path = EXAMPLE_PATH / "results" / "e_coli_core"

    curator_cobrapy = CuratorCobrapy(model_path=model_path)
    res_cobra = curator_cobrapy.run()
    res_cobra.write_results(results_path / "cobrapy")
    res_cobra2 = CuratorResult.read_results(results_path / "cobrapy")


    curator_cameo = CuratorCameo(model_path=model_path)
    res_cameo = curator_cameo.run()
    res_cameo.write_results(results_path / "cameo")
    res_cameo2 = CuratorResult.read_results(results_path / "cameo")

    # store results

    # comparison
