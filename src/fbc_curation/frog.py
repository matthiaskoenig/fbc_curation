"""FROG schema definition."""
import hashlib
import os
import platform
from pathlib import Path
from typing import Optional, List

from pydantic import BaseModel, Field
from pymetadata.console import console

from datetime import date


class Creator(BaseModel):
    """Creator/curator in ModelHistory and other COMBINE formats.

    Extended by optional orcid.
    """

    familyName: str
    givenName: str
    email: Optional[str]
    organization: Optional[str]
    site: Optional[str]
    orcid: Optional[str]


class Tool(BaseModel):
    name: str = Field(description="Name of tool/software/library.")
    version: Optional[str] = Field(description="Version of tool/software/library.")
    url: Optional[str] = Field(description="URL of tool/software/library.")


class FrogMetaData(BaseModel):
    """FROG metadata."""

    frog_date: date = Field(
        alias="frog.date",
        description="Curators which executed the FROG analysis."
    )
    frog_version: str = Field(
        title="FROG version",
        alias="frog.version",
        description="Version of FROG according to schema.",
    )
    frog_curators: List[Creator] = Field(
        alias="frog.curators",
        description="Curators which executed the FROG analysis."
    )
    frog_software: Tool = Field(
        alias="frog.software",
        description="Software used to run FROG",
    )
    software: Tool = Field(
        description="Software used to run FBC."
    )
    solver: Tool = Field(
        description="Solver used to solve LP problem (e.g. CPLEX, GUROBI, GLPK)."
    )
    model_filename: str = Field(alias="model.filename")
    model_md5: str = Field(alias="model.md5")
    environment: Optional[str] = Field(
        description="Execution environment such as Linux."
    )

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


from pymetadata.console import console
from pydantic import BaseModel
import numpy as np
from enum import Enum


class StatusCode(str, Enum):
    OPTIMAL = "optimal"
    INFEASIBLE = "infeasible"


class FrogObjective(BaseModel):
    model: str
    objective: str
    status: StatusCode
    value: float


class FrogFVASingle(BaseModel):
    model: str
    objective: str
    reaction: str
    flux: float
    status: StatusCode
    minimum: float
    maximum: float
    fraction_optimum: float


class FrogReactionDeletion(BaseModel):
    model: str
    objective: str
    gene: str
    status: StatusCode
    value: float


class FrogGeneDeletion(BaseModel):
    model: str
    objective: str
    gene: str
    status: StatusCode
    value: float


class Frog(BaseModel):
    metadata: FrogMetaData
    objective: FrogObjective
    fva: List[FrogFVASingle]
    reaction_deletions: List[FrogReactionDeletion]
    gene_deletions: List[FrogGeneDeletion]



if __name__ == "__main__":

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
            name="glpk",
            version=f"{GLP_MAJOR_VERSION}.{GLP_MINOR_VERSION}",
            url=None
        ),
        environment=f"{os.name}, {platform.system()}, {platform.release()}",
        model_filename=ecoli_path.name,
        model_md5=FrogMetaData.md5_for_path(ecoli_path),
    )

    console.print(metadata)
    console.print(metadata.dict(by_alias=True))
    console.print(FrogMetaData.schema_json(indent=2))
    console.print(Frog.schema_json(indent=2))
