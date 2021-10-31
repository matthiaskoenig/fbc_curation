"""FROG schema definition."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import tempfile
from datetime import date
from enum import Enum
from math import isnan
from pathlib import Path
from typing import Any, List, Optional, Dict

import numpy as np
import pandas as pd
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, validator
from pymetadata import log
from pymetadata.console import console
from pymetadata.omex import EntryFormat, ManifestEntry, Omex


logger = log.get_logger(__name__)

# ----------------------------------------------
# Handling NaNs via https://github.com/samuelcolvin/pydantic/issues/1779
# FIXME: get rid of this information !!!


class BaseModel(PydanticBaseModel):
    @validator("*")
    def change_nan_to_none(cls, v: Any, field: Any) -> Any:
        if field.outer_type_ is float and isnan(v):
            return None
        return v


class CuratorConstants:
    """Class storing constants for curation and file format."""
    FROG_KEY = "frog"
    METADATA_KEY = "metadata"
    OBJECTIVE_KEY = "objective"
    FVA_KEY = "fva"
    GENEDELETIONS_KEY = "gene_deletion"
    REACTIONDELETIONS_KEY = "reaction_deletion"

    # output filenames
    FROG_FILENAME = "frog.json"
    METADATA_FILENAME = "metadata.json"
    OBJECTIVE_FILENAME = f"01_{OBJECTIVE_KEY}.tsv"
    FVA_FILENAME = f"02_{FVA_KEY}.tsv"
    GENEDELETIONS_FILENAME = f"03_{GENEDELETIONS_KEY}.tsv"
    REACTIONDELETIONS_FILENAME = f"04_{REACTIONDELETIONS_KEY}.tsv"


    # special settings for comparison
    VALUE_INFEASIBLE = np.NaN


class StatusCode(str, Enum):
    OPTIMAL: str = "optimal"
    INFEASIBLE: str = "infeasible"


class FrogObjective(BaseModel):
    model: str
    objective: str
    status: StatusCode
    value: float

    class Config:
        use_enum_values = True


class FrogFVASingle(BaseModel):
    model: str
    objective: str
    reaction: str
    flux: float
    status: StatusCode
    minimum: float
    maximum: float
    fraction_optimum: float

    class Config:
        use_enum_values = True


class FrogReactionDeletion(BaseModel):
    model: str
    objective: str
    reaction: str
    status: StatusCode
    value: float

    class Config:
        use_enum_values = True


class FrogGeneDeletion(BaseModel):
    model: str
    objective: str
    gene: str
    status: StatusCode
    value: float

    class Config:
        use_enum_values = True


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

    class Config:
        use_enum_values = True


class Tool(BaseModel):
    name: str = Field(description="Name of tool/software/library.")
    version: Optional[str] = Field(description="Version of tool/software/library.")
    url: Optional[str] = Field(description="URL of tool/software/library.")

    class Config:
        use_enum_values = True


class FrogMetaData(BaseModel):
    """FROG metadata."""

    model_location: str = Field(
        alias="model.location",
        description="Location of the model in the COMBINE archive for which the FROG "
                    "analysis was performed."
    )
    frog_id: str = Field(
        description="Id for the FROG analysis. All frog_ids within an archive must be "
                    "unique."
    )
    frog_curators: List[Creator] = Field(
        alias="frog.curators", description="Curators which executed the FROG analysis."
    )
    frog_software: Tool = Field(
        alias="frog.software",
        description="Software used to run FROG (e.g. 'fbc_curation'",
    )
    software: Tool = Field(
        description="Software used to run FBC (e.g. 'cameo', 'COBRA', 'cobrapy'"
    )
    solver: Tool = Field(
        description="Solver used to solve LP problem (e.g. 'CPLEX', 'GUROBI', 'GLPK')."
    )
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
    """Definition of FROG FVA."""

    fva: List[FrogFVASingle]

    class Config:
        use_enum_values = True


class FrogReactionDeletions(BaseModel):
    """Definition of FROG Reaction deletions."""

    deletions: List[FrogReactionDeletion]

    class Config:
        use_enum_values = True


class FrogGeneDeletions(BaseModel):
    """Definition of FROG Gene deletions."""

    deletions: List[FrogGeneDeletion]

    class Config:
        use_enum_values = True


class FrogReport(BaseModel):
    """Definition of the FROG standard."""

    metadata: FrogMetaData
    objective: FrogObjective
    fva: FrogFVA
    reaction_deletions: FrogReactionDeletions
    gene_deletions: FrogGeneDeletions

    class Config:
        use_enum_values = True

    def to_json(self, path: Path) -> None:
        """Write FrogReport to JSON format."""
        if not path.parent.exists():
            logger.warning(f"Creating results path: {path.parent}")
            path.mkdir(parents=True)

        # write FROG
        logger.debug(f"{path}")
        with open(path, "w") as f_json:
            f_json.write(self.json(indent=2))

    @staticmethod
    def from_json(path: Path) -> FrogReport:
        """Read FrogReport from JSON format.

        raises ValidationError

        :path: path to JSON report file
        """
        with open(path, "r") as f_json:
            d = json.load(fp=f_json)
            return FrogReport(**d)

    def to_dfs(self) -> Dict[str, pd.DataFrame]:
        """Create report DataFrames."""

        dfs: Dict[str, pd.DataFrame] = {}
        for key, data in dict(
            zip(
                [
                    CuratorConstants.OBJECTIVE_KEY,
                    CuratorConstants.FVA_KEY,
                    CuratorConstants.GENEDELETIONS_KEY,
                    CuratorConstants.REACTIONDELETIONS_KEY,
                ],
                [
                    self.objective,
                    self.fva,
                    self.gene_deletions,
                    self.reaction_deletions,
                ],
            )
        ).items():

            d = data.dict()
            if key == CuratorConstants.OBJECTIVE_KEY:
                df = pd.DataFrame.from_records([d])
                df.sort_values(by=["objective"], inplace=True)
                df.index = range(len(df))
            else:
                item = list(d.values())[0]
                df = pd.DataFrame(item)
                if key in {
                    CuratorConstants.FVA_KEY,
                    CuratorConstants.REACTIONDELETIONS_KEY,
                }:
                    df.sort_values(by=["reaction"], inplace=True)
                    df.index = range(len(df))
                elif key == CuratorConstants.GENEDELETIONS_KEY:
                    df.sort_values(by=["gene"], inplace=True)
                    df.index = range(len(df))

            if key in [
                CuratorConstants.OBJECTIVE_KEY,
                CuratorConstants.REACTIONDELETIONS_KEY,
                CuratorConstants.GENEDELETIONS_KEY,
            ]:
                df.loc[
                    df.status == StatusCode.INFEASIBLE.value, "value"
                ] = CuratorConstants.VALUE_INFEASIBLE
            elif key == CuratorConstants.FVA_KEY:
                df.loc[
                    df.status == StatusCode.INFEASIBLE.value, ["flux", "minimum", "maximum"]
                ] = CuratorConstants.VALUE_INFEASIBLE

            df[key] = df
        return dfs

    def to_tsv(self, output_dir: Path) -> None:
        """Write Report TSV and metadata to directory"""
        if not output_dir.exists():
            logger.warning(f"Creating results path: {output_dir}")
            output_dir.mkdir(parents=True)

        # write metadata file
        logger.debug(f"{output_dir / CuratorConstants.METADATA_FILENAME}")
        with open(output_dir / CuratorConstants.METADATA_FILENAME, "w") as f_json:
            f_json.write(self.metadata.json(indent=2))

        # write reference files (TSV files)
        dfs_dict = self.to_dfs()
        for key, df in dfs_dict.items():
            if key == CuratorConstants.OBJECTIVE_KEY:
                filename = CuratorConstants.OBJECTIVE_FILENAME
            elif key == CuratorConstants.FVA_KEY:
                filename = CuratorConstants.FVA_FILENAME
            elif key == CuratorConstants.GENEDELETIONS_KEY:
                filename = CuratorConstants.GENEDELETIONS_FILENAME
            elif key == CuratorConstants.REACTIONDELETIONS_KEY:
                filename = CuratorConstants.REACTIONDELETIONS_FILENAME

            df.to_csv(output_dir / filename, sep="\t", index=False, na_rep="NaN")

    @classmethod
    def from_tsv(cls, path_in: Path) -> "FrogReport":
        """Read fbc curation files from given directory."""
        # FIXME: implement

        path_metadata = path_in / CuratorConstants.METADATA_FILENAME
        path_objective = path_in / CuratorConstants.OBJECTIVE_FILENAME
        path_fva = path_in / CuratorConstants.FVA_FILENAME
        path_gene_deletion = path_in / CuratorConstants.GENEDELETIONS_FILENAME
        path_reaction_deletion = path_in / CuratorConstants.REACTIONDELETIONS_FILENAME
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

        return FrogReport(objective_id=objective_id, **df_dict)

    def to_omex(self, omex: Omex, location_prefix="./FROG/") -> None:
        """Add report to omex.

        :param omex: OMEX archive to add report to.
        :param location_prefix: prefix to where to write the FROG files in the OMEX
        """
        # TODO: create new omex with model if not existing

        with tempfile.TemporaryDirectory() as f_tmp:
            tmp_path: Path = Path(f_tmp)

            # write json
            json_path = tmp_path / CuratorConstants.FROG_FILENAME
            self.to_json(json_path)
            omex.add_entry(
                entry_path=json_path,
                entry=ManifestEntry(
                    location=f"{location_prefix}{CuratorConstants.FROG_FILENAME}",
                    format=EntryFormat.FROG_JSON_V1,
                ),
            )

            # write tsvs with metadata
            self.to_tsv(tmp_path)
            for filename, format in [
                (
                    CuratorConstants.METADATA_FILENAME,
                    EntryFormat.FROG_METADATA_V1,
                ),
                (
                    CuratorConstants.OBJECTIVE_FILENAME,
                    EntryFormat.FROG_OBJECTIVE_V1,
                ),
                (CuratorConstants.FVA_FILENAME, EntryFormat.FROG_FVA_V1),
                (
                    CuratorConstants.REACTIONDELETIONS_FILENAME,
                    EntryFormat.FROG_REACTIONDELETION_V1,
                ),
                (
                    CuratorConstants.GENEDELETIONS_FILENAME,
                    EntryFormat.FROG_GENEDELETION_V1,
                ),
            ]:
                omex.add_entry(
                    entry_path=tmp_path / filename,
                    entry=ManifestEntry(
                        location=f"{location_prefix}{filename}",
                        format=format,
                    ),
                )

    def from_omex(self, omex_path) -> List[FrogReport]:
        """Read report from OMEX files"""
        pass


if __name__ == "__main__":

    console.rule(style="white")
    console.print(FrogReport.schema_json(indent=2))
    console.rule(style="white")
    with open("frog-schema-version1.json", "w") as f_schema:
        f_schema.write(FrogReport.schema_json(indent=2))
