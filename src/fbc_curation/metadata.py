"""Create metadata information."""
import hashlib
import os
import platform
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
from pymetadata.console import console


class FROGMetaData(BaseModel):
    """FROG metadata."""
    curator_name: str = Field(
        alias="curator.name",
        description="Name of curation tool used to create the FROG report.",
    )
    curator_version: Optional[str] = Field(
        alias="curator.version",
        description="Version of curation tool used to create the FROG report.",
    )
    curator_url: Optional[str] = Field(
        alias="curator.url",
        description="URL of curation tool used to create the FROG report.",
    )
    software_name: str = Field(alias="software.name")
    software_version: str = Field(alias="software.version")
    software_url: Optional[str] = Field(alias="software.url")

    solver_name: str = Field(alias="solver.name")
    solver_version: Optional[str] = Field(alias="solver.version")
    solver_url: Optional[str] = Field(alias="solver.url")

    model_filename: str = Field(alias="model.filename")
    model_md5: str = Field(alias="model.md5")

    environment: str

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True

    @staticmethod
    def md5_for_path(path: Path) -> str:
        """Calculate MD5 of file content."""

        # Open,close, read file and calculate MD5 on its contents
        with open(path, "rb") as f_check:
            # read contents of the file
            data = f_check.read()
            # pipe contents of the file through
            return hashlib.md5(data).hexdigest()


if __name__ == "__main__":

    from fbc_curation import EXAMPLE_PATH
    from swiglpk import GLP_MAJOR_VERSION, GLP_MINOR_VERSION
    from cobra import __version__ as cobra_version
    from fbc_curation import __citation__, __software__, __version__

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

    console.print(metadata)
    console.print(metadata.dict(by_alias=True))

    console.print(FROGMetaData.schema_json(indent=2))
