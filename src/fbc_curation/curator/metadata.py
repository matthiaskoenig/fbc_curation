"""Create metadata information."""
import hashlib
import os
import platform
from pathlib import Path

from pymetadata.console import console

from fbc_curation import __citation__, __software__, __version__


def create_metadata(path: Path):
    """Create curation metadata for given model."""
    d = {}
    d["software.name"] = __software__
    d["software.version"] = __version__
    d["software.url"] = __citation__
    d["environment"] = f"{os.name}, {platform.system()}, {platform.release()}"
    d["model.filename"] = path.name
    d["model.md5"] = md5_for_path(path)
    d["solver.name"] = None
    d["solver.version"] = None

    return d


def md5_for_path(path: Path):
    """Calculate MD5 of file content."""

    # Open,close, read file and calculate MD5 on its contents
    with open(path, "rb") as f_check:
        # read contents of the file
        data = f_check.read()
        # pipe contents of the file through
        return hashlib.md5(data).hexdigest()


def filename_for_path(path: Path):
    """Return filename of path."""
    return path.name


if __name__ == "__main__":

    from fbc_curation import EXAMPLE_PATH

    ecoli_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"
    d = create_metadata(path=ecoli_path)
    console.print(d)
