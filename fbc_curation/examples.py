"""
Create curation information for example models.
"""
from fbc_curation import EXAMPLE_PATH
from fbc_curation.fbc_files import FBCFileCreator


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


def run_examples(results_path):
    example_ecoli_core(results_path / "e_coli_core")
    example_iJR904(results_path / "iJR904")
    example_MODEL1709260000(results_path / "MODEL1709260000")


if __name__ == "__main__":
    run_examples(EXAMPLE_PATH / "results")
