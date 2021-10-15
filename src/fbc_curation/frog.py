"""FROG schema definition."""
import hashlib
import os
import platform
from pathlib import Path
from typing import Optional, List

import numpy as np
from pydantic import BaseModel, Field
from datetime import date

from pymetadata.console import console

from enum import Enum
from pymetadata import log

logger = log.get_logger(__name__)


# ----------------------------------------------
# FIXME: get rid of this information !!!


class CuratorConstants:
    """Class storing constants for curation and file format."""

    # keys of outputs
    METADATA_KEY = "metadata"
    OBJECTIVE_KEY = "objective"
    FVA_KEY = "fva"
    GENE_DELETION_KEY = "gene_deletion"
    REACTION_DELETION_KEY = "reaction_deletion"

    # output filenames
    METADATA_FILENAME = "metadata.json"
    OBJECTIVE_FILENAME = f"01_{OBJECTIVE_KEY}.tsv"
    FVA_FILENAME = f"02_{FVA_KEY}.tsv"
    GENE_DELETION_FILENAME = f"03_{GENE_DELETION_KEY}.tsv"
    REACTION_DELETION_FILENAME = f"04_{REACTION_DELETION_KEY}.tsv"

    FILENAMES = [
        OBJECTIVE_FILENAME,
        FVA_FILENAME,
        GENE_DELETION_FILENAME,
        REACTION_DELETION_FILENAME,
    ]

    # fields

    FVA_FIELDS = [
        "model",
        "objective",
        "reaction",
        "flux",
        "status",
        "minimum",
        "maximum",
        "fraction_optimum",
    ]
    GENE_DELETION_FIELDS = ["model", "objective", "gene", "status", "value"]
    REACTION_DELETION_FIELDS = ["model", "objective", "reaction", "status", "value"]

    # special settings for comparison
    VALUE_INFEASIBLE = np.NaN
    NUM_DECIMALS = 6  # decimals to write in the solution


# ----------------------------------------------


# FIXME: how to define an enum
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
    reaction: str
    status: StatusCode
    value: float


class FrogGeneDeletion(BaseModel):
    model: str
    objective: str
    gene: str
    status: StatusCode
    value: float


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
        alias="frog.date", description="Curators which executed the FROG analysis."
    )
    frog_version: str = Field(
        title="FROG version",
        alias="frog.version",
        description="Version of FROG according to schema.",
    )
    frog_curators: List[Creator] = Field(
        alias="frog.curators", description="Curators which executed the FROG analysis."
    )
    frog_software: Tool = Field(
        alias="frog.software",
        description="Software used to run FROG",
    )
    software: Tool = Field(description="Software used to run FBC.")
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


class FrogFVA(BaseModel):
    fva: List[FrogFVASingle]


class FrogReactionDeletions(BaseModel):
    deletions: List[FrogReactionDeletion]


class FrogGeneDeletions(BaseModel):
    deletions: List[FrogGeneDeletion]


class FrogReport(BaseModel):
    """Definition of the FROG standard."""
    metadata: FrogMetaData
    objective: FrogObjective
    fva: FrogFVA
    reaction_deletions: FrogReactionDeletions
    gene_deletions: FrogGeneDeletions


    # FIXME: update the reading & writing of files

    def write_results(self, path_out: Path):
        """Write results to path."""
        if not path_out.exists():
            logger.warning(f"Creating results path: {path_out}")
            path_out.mkdir(parents=True)

        # write metadata file
        with open(path_out / CuratorConstants.METADATA_FILENAME, "w") as f_json:
            json.dump(self.metadata, fp=f_json, indent=2)

        # write reference files
        for filename, df in dict(
            zip(
                [
                    CuratorConstants.OBJECTIVE_FILENAME,
                    CuratorConstants.FVA_FILENAME,
                    CuratorConstants.GENE_DELETION_FILENAME,
                    CuratorConstants.REACTION_DELETION_FILENAME,
                ],
                [self.objective, self.fva, self.gene_deletion, self.reaction_deletion],
            )
        ).items():
            logger.debug(f"-> {path_out / filename}")
            df.to_csv(path_out / filename, sep="\t", index=False)
            # df.to_json(path_out / filename, sep="\t", index=False)

    @classmethod
    def read_results(cls, path_in: Path):
        """Read fbc curation files from given directory."""
        path_metadata = path_in / CuratorConstants.METADATA_FILENAME
        path_objective = path_in / CuratorConstants.OBJECTIVE_FILENAME
        path_fva = path_in / CuratorConstants.FVA_FILENAME
        path_gene_deletion = path_in / CuratorConstants.GENE_DELETION_FILENAME
        path_reaction_deletion = path_in / CuratorConstants.REACTION_DELETION_FILENAME
        df_dict = dict()

        for k, path in enumerate(
            [path_objective, path_fva, path_gene_deletion, path_reaction_deletion]
        ):
            if not path_objective.exists():
                logger.error(f"Required file for fbc curation does not exist: '{path}'")
            else:
                df_dict[CuratorConstants.KEYS[k]] = pd.read_csv(path, sep="\t")

        with open(path_metadata, "r") as f_json:
            df_dict[CuratorConstants.METADATA_KEY] = json.load(fp=f_json)
        objective_id = df_dict["objective"].objective.values[0]

        return FROGResults(objective_id=objective_id, **df_dict)


if __name__ == "__main__":

    console.rule(style="white")
    console.print(FrogReport.schema_json(indent=2))
    console.rule(style="white")
    with open("frog-schema-version1.json", "w") as f_schema:
        f_schema.write(FrogReport.schema_json(indent=2))
