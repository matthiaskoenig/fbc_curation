from datetime import date

import pytest
import os
import platform
from fbc_curation import __citation__, __software__, __version__
from fbc_curation.metadata import FrogMetaData, Creator, Tool


def test_frog_metadata() -> None:
    from fbc_curation import EXAMPLE_PATH
    from swiglpk import GLP_MAJOR_VERSION, GLP_MINOR_VERSION
    from cobra import __version__ as cobra_version
    from fbc_curation import __citation__, __software__, __version__

    ecoli_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"
    metadata = FrogMetaData(
        frog_date=date(year=2021, month=10, day=11),
        frog_version="1.0",
        frog_curators=[
            Creator(
                givenName="Matthias",
                familyName="König",
                organization="Humboldt University Berlin",
                site="https://livermetabolism.com",
                orcid="0000-0003-1725-179X",
            )
        ],
        frog_software=Tool(
            name=__software__,
            version=__version__,
            url=__citation__,
        ),
        software=Tool(
            name="cobrapy",
            version=cobra_version,
            url="https://github.com/opencobra/cobrapy",
        ),
        solver=Tool(
            name="glpk", version=f"{GLP_MAJOR_VERSION}.{GLP_MINOR_VERSION}", url=None
        ),
        environment=f"{os.name}, {platform.system()}, {platform.release()}",
        model_filename=ecoli_path.name,
        model_md5=FrogMetaData.md5_for_path(ecoli_path),
    )
    assert metadata
    assert metadata.curator_version
