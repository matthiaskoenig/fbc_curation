from pathlib import Path
from fbc_curation import create_fbc_files


def example_ecoli_core(results_dir):
    """Create example files for ecoli core."""
    model_path = Path(__file__).parent / "models" / "e_coli_core.xml"
    create_fbc_files(results_dir=results_dir, model_path=model_path)


def example_iJR904(results_dir):
    """Create example files for ecoli core."""
    model_path = Path(__file__).parent / "models" / "iJR904.xml.gz"
    create_fbc_files(results_dir=results_dir, model_path=model_path)


if __name__ == "__main__":
    results_dir = Path(__file__).parent / "results"
    example_ecoli_core(results_dir)
    # example_iJR904(results_dir)
