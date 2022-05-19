"""Test metadata."""

import os
import platform
from datetime import date

from fbc_curation.frog import Creator, FrogMetaData, Tool


def test_frog_metadata() -> None:
    """Test metadata."""
    from cobra import __version__ as cobra_version
    from swiglpk import GLP_MAJOR_VERSION, GLP_MINOR_VERSION

    from fbc_curation import EXAMPLE_DIR, __citation__, __software__, __version__

    ecoli_path = EXAMPLE_DIR / "models" / "e_coli_core.xml"
    metadata = FrogMetaData(
        frog_id="8743b52063cd84097a65d1633f5c74f5",
        frog_date=date(year=2021, month=10, day=11),
        frog_version="1.0",
        curators=[
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
        model_location=ecoli_path.name,
        model_filename=ecoli_path.name,
        model_md5=FrogMetaData.md5_for_path(ecoli_path),
    )
    assert metadata
