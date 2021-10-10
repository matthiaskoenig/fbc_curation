import pytest
import os
import platform
from fbc_curation import __citation__, __software__, __version__
from fbc_curation.metadata import FROGMetaData


def test_frog_metadata() -> None:
    from fbc_curation import EXAMPLE_PATH
    from swiglpk import GLP_MAJOR_VERSION, GLP_MINOR_VERSION
    from cobra import __version__ as cobra_version

    ecoli_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"
    metadata = FROGMetaData(
        curator_name=__software__,
        curator_version=__version__,
        curator_url=__citation__,
        software_name="cobrapy",
        software_version=cobra_version,
        software_url="https://github.com/opencobra/cobrapy",
        environment=f"{os.name}, {platform.system()}, {platform.release()}",
        model_filename=ecoli_path.name,
        model_md5=FROGMetaData.md5_for_path(ecoli_path),
        solver_name="glpk",
        solver_version=f"{GLP_MAJOR_VERSION}.{GLP_MINOR_VERSION}",
    )
    assert metadata
    assert metadata.curator_version
