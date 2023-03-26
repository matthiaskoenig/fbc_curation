"""Helper script for running multiple frog analysis."""
from pathlib import Path

from fbc_curation.worker import run_frog
from pymetadata.omex import Omex


def runfrogs(models_dir: Path, extract_omex: bool = True):
    """Run FROG reports for models.
    """
    print(models_dir)
    models = models_dir.glob('*/*.xml')
    for model_path in models:
        omex_path = model_path.parent / f"{model_path.stem}_FROG.omex"
        print(f"{model_path} -> {omex_path}")
        run_frog(
            source_path=model_path,
            omex_path=omex_path,
        )
        if extract_omex:
            omex = Omex.from_omex(omex_path)
            omex.to_directory(model_path.parent)


if __name__ == "__main__":
    models_dir: Path = Path("/home/mkoenig/Downloads/frog/models/")
    runfrogs(models_dir=models_dir)
