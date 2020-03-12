"""
Create curation information for example models.
"""

from fbc_curation import EXAMPLE_PATH
from fbc_curation.fbc_files import create_fbc_files


def example_ecoli_core(results_dir):
    """Create example files for ecoli core."""
    model_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"
    create_fbc_files(results_dir=results_dir, model_path=model_path)


def example_iJR904(results_dir):
    """Create example files for ecoli core."""
    model_path = EXAMPLE_PATH / "models" / "iJR904.xml.gz"
    create_fbc_files(results_dir=results_dir, model_path=model_path)

def run_examples():
    results_dir = EXAMPLE_PATH / "results"
    example_ecoli_core(results_dir)
    example_iJR904(results_dir)


if __name__ == "__main__":
    run_examples()
