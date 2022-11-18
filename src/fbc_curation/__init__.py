from pathlib import Path

__software__ = "fbc_curation"
__version__ = "0.2.1"
__citation__ = "https://doi.org/10.5281/zenodo.3708271"


RESOURCES_DIR = Path(__file__).parent / "resources"
EXAMPLE_DIR = RESOURCES_DIR / "examples"

FROG_SCHEMA_VERSION_1 = RESOURCES_DIR / "schema" / "frog-schema-version-1.json"
FROG_DATA_DIR = Path(__file__).parent.parent / "frog_data"

FROG_PATH_PREFIX = "FROG"
