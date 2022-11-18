"""FROG schema definition."""
from __future__ import annotations

import hashlib
import tempfile
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import orjson
import pandas as pd
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, ValidationError, validator
from pymetadata import log
from pymetadata.omex import EntryFormat, ManifestEntry, Omex

from fbc_curation import FROG_PATH_PREFIX


logger = log.get_logger(__name__)


class BaseModel(PydanticBaseModel):
    """Base model."""

    # pass
    @validator("*")
    def change_nan_to_none(cls, v: Any, field: Any) -> Any:
        """Replace NaN to None values."""
        if (field.outer_type_ is float) and (v is not None) and (np.isnan(v)):
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
    """Status code for simulation results."""

    OPTIMAL: str = "optimal"
    INFEASIBLE: str = "infeasible"


class FrogObjective(BaseModel):
    """Frog Objective."""

    model: str
    objective: str
    status: StatusCode
    value: float

    class Config:
        """Pydantic configuration FrogObjective."""

        use_enum_values = True


class FrogFVASingle(BaseModel):
    """Frog FVA."""

    model: str
    objective: str
    reaction: str
    flux: Optional[float]
    status: StatusCode
    minimum: Optional[float]
    maximum: Optional[float]
    fraction_optimum: float

    class Config:
        """Pydantic configuration FrogFVA."""

        use_enum_values = True


class FrogReactionDeletion(BaseModel):
    """Frog reaction deletion."""

    model: str
    objective: str
    reaction: str
    status: StatusCode
    value: Optional[float]

    class Config:
        """Pydantic configuration FrogGeneDeletion."""

        use_enum_values = True


class FrogGeneDeletion(BaseModel):
    """Frog gene deletion."""

    model: str
    objective: str
    gene: str
    status: StatusCode
    value: Optional[float]

    class Config:
        """Pydantic configuration FrogGeneDeletion."""

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
        """Pydantic configuration Creator."""

        use_enum_values = True


class Tool(BaseModel):
    """Tool description."""

    name: str = Field(description="Name of tool/software/library.")
    version: Optional[str] = Field(description="Version of tool/software/library.")
    url: Optional[str] = Field(description="URL of tool/software/library.")

    class Config:
        """Pydantic configuration FrogFVA."""

        use_enum_values = True


class FrogMetaData(BaseModel):
    """FROG metadata."""

    model_location: str = Field(
        alias="model.location",
        description="Location of the model in the COMBINE archive for which the FROG "
        "analysis was performed.",
    )
    model_md5: Optional[str] = Field(
        alias="model.md5",
        description="MD5 hash of model",
    )
    frog_id: str = Field(
        description="Id for the FROG analysis. All frog_ids within an archive must be "
        "unique."
    )
    frog_software: Tool = Field(
        alias="frog.software",
        description="Software used to run FROG (e.g. 'fbc_curation'",
    )
    curators: List[Creator] = Field(
        alias="frog.curators", description="Curators which executed the FROG analysis."
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
        """Pydantic configuration FrogMetaData."""

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


class FrogObjectives(BaseModel):
    """Definition of FROG Objectives."""

    objectives: List[FrogObjective]

    class Config:
        """Pydantic configuration FrogObjectives."""

        use_enum_values = True

    @staticmethod
    def from_df(df: pd.DataFrame) -> FrogObjectives:
        """Parse Objectives from DataFrame."""
        json = df.to_dict(orient="records")
        objectives = []
        for item in json:
            try:
                objectives.append(FrogObjective(**item))
            except ValidationError as e:
                logger.error(item)
                logger.error(e.json())

        return FrogObjectives(objectives=objectives)

    def to_df(self) -> pd.DataFrame:
        """Create objectives DataFrame."""

        d: Dict[str, Any] = self.dict()
        item = list(d.values())[0]
        df = pd.DataFrame(item)
        if len(df) > 0:
            df.sort_values(by=["objective"], inplace=True)
            df.index = range(len(df))
            df.loc[
                df.status == StatusCode.INFEASIBLE.value, "value"
            ] = CuratorConstants.VALUE_INFEASIBLE

        return df


class FrogFVA(BaseModel):
    """Definition of FROG FVA."""

    fva: List[FrogFVASingle]

    class Config:
        """Pydantic configuration FrogFVA."""

        use_enum_values = True

    @staticmethod
    def from_df(df: pd.DataFrame) -> FrogFVA:
        """Parse FVA from DataFrame."""

        fva = []
        for item in df.to_dict(orient="records"):
            try:
                fva.append(FrogFVASingle(**item))
            except ValidationError as e:
                logger.error(item)
                logger.error(e.json())
        return FrogFVA(fva=fva)

    def to_df(self) -> pd.DataFrame:
        """Create fva DataFrame."""

        d: Dict[str, Any] = self.dict()
        item = list(d.values())[0]
        df = pd.DataFrame(item)
        if len(df) > 0:
            df.sort_values(by=["reaction"], inplace=True)
            df.index = range(len(df))
            df.loc[
                df.status == StatusCode.INFEASIBLE.value,
                ["flux", "minimum", "maximum"],
            ] = CuratorConstants.VALUE_INFEASIBLE

        return df


class FrogReactionDeletions(BaseModel):
    """Definition of FROG Reaction deletions."""

    deletions: List[FrogReactionDeletion]

    class Config:
        """Pydantic configuration FrogReactionDeletions."""

        use_enum_values = True

    @staticmethod
    def from_df(df: pd.DataFrame) -> FrogReactionDeletions:
        """Parse FVA from DataFrame."""
        json = df.to_dict(orient="records")
        deletions = []
        for item in json:
            try:
                deletions.append(FrogReactionDeletion(**item))
            except ValidationError as e:
                logger.error(item)
                logger.error(e.json())

        return FrogReactionDeletions(deletions=deletions)

    def to_df(self) -> pd.DataFrame:
        """Create reaction deletions DataFrame."""

        d: Dict[str, Any] = self.dict()
        item = list(d.values())[0]
        df = pd.DataFrame(item)
        if len(df) > 0:
            df.sort_values(by=["reaction"], inplace=True)
            df.index = range(len(df))
            df.loc[
                df.status == StatusCode.INFEASIBLE.value, "value"
            ] = CuratorConstants.VALUE_INFEASIBLE

        return df


class FrogGeneDeletions(BaseModel):
    """Definition of FROG Gene deletions."""

    deletions: List[FrogGeneDeletion]

    class Config:
        """Pydantic configuration FrogGeneDeletions."""

        use_enum_values = True

    @staticmethod
    def from_df(df: pd.DataFrame) -> FrogGeneDeletions:
        """Parse GeneDeletions from DataFrame."""
        json = df.to_dict(orient="records")
        deletions = []
        for item in json:
            try:
                deletions.append(FrogGeneDeletion(**item))
            except ValidationError as e:
                logger.error(item)
                logger.error(e.json())

        return FrogGeneDeletions(deletions=deletions)

    def to_df(self) -> pd.DataFrame:
        """Create gene deletions DataFrame."""

        d: Dict[str, Any] = self.dict()
        item = list(d.values())[0]
        df = pd.DataFrame(item)
        if len(df) > 0:
            df.sort_values(by=["gene"], inplace=True)
            df.index = range(len(df))
            df.loc[
                df.status == StatusCode.INFEASIBLE.value, "value"
            ] = CuratorConstants.VALUE_INFEASIBLE

        return df


class FrogReport(BaseModel):
    """Definition of the FROG standard."""

    metadata: FrogMetaData
    objectives: FrogObjectives
    fva: FrogFVA
    reaction_deletions: FrogReactionDeletions
    gene_deletions: FrogGeneDeletions

    class Config:
        """Pydantic configuration FrogReport."""

        use_enum_values = True

    def to_json(self, path: Path) -> None:
        """Write FrogReport to JSON format."""
        if not path.parent.exists():
            logger.warning(f"Creating results path: {path.parent}")
            path.mkdir(parents=True)

        # write FROG
        logger.debug(f"{path}")
        with open(path, "w+b") as f_json:
            json_bytes = orjson.dumps(self.dict(), option=orjson.OPT_INDENT_2)
            f_json.write(json_bytes)

    @staticmethod
    def from_json(path: Path) -> FrogReport:
        """Read FrogReport from JSON format.

        raises ValidationError

        :path: path to JSON report file
        """
        with open(path, "r+b") as f_json:
            s_json = f_json.read()
            d = orjson.loads(s_json)
            return FrogReport(**d)

    def to_dfs(self) -> Dict[str, pd.DataFrame]:
        """Create report DataFrames."""

        return {
            CuratorConstants.OBJECTIVE_KEY: self.objectives.to_df(),
            CuratorConstants.FVA_KEY: self.fva.to_df(),
            CuratorConstants.GENEDELETIONS_KEY: self.gene_deletions.to_df(),
            CuratorConstants.REACTIONDELETIONS_KEY: self.reaction_deletions.to_df(),
        }

    def to_tsv(self, output_dir: Path) -> None:
        """Write Report TSV and metadata to directory."""
        if not output_dir.exists():
            logger.warning(f"Creating results path: {output_dir}")
            output_dir.mkdir(parents=True)

        # write metadata file
        logger.debug(f"{output_dir / CuratorConstants.METADATA_FILENAME}")
        with open(output_dir / CuratorConstants.METADATA_FILENAME, "w") as f_json:
            # make a copy
            metadata = FrogMetaData(**self.metadata.dict())
            metadata.frog_id = f"{metadata.frog_id}_tsv"
            f_json.write(metadata.json(indent=2))

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
    def from_tsv(cls, path: Path) -> FrogReport:
        """Read fbc curation files from given directory."""

        path_metadata = path / CuratorConstants.METADATA_FILENAME
        path_objective = path / CuratorConstants.OBJECTIVE_FILENAME
        path_fva = path / CuratorConstants.FVA_FILENAME
        path_reaction_deletion = path / CuratorConstants.REACTIONDELETIONS_FILENAME
        path_gene_deletion = path / CuratorConstants.GENEDELETIONS_FILENAME
        df_dict: Dict[str, pd.DataFrame] = dict()

        with open(path_metadata, "r+b") as f_json:
            json_bytes = f_json.read()
            df_dict[CuratorConstants.METADATA_KEY] = orjson.loads(json_bytes)

        for key, path in {
            CuratorConstants.OBJECTIVE_KEY: path_objective,
            CuratorConstants.FVA_KEY: path_fva,
            CuratorConstants.REACTIONDELETIONS_KEY: path_reaction_deletion,
            CuratorConstants.GENEDELETIONS_KEY: path_gene_deletion,
        }.items():
            if not path.exists():
                logger.error(f"Required file for fbc curation does not exist: '{path}'")
            else:
                try:
                    df_dict[key] = pd.read_csv(path, sep="\t")
                except pd.errors.EmptyDataError:
                    df_dict[key] = pd.DataFrame()

        report = FrogReport(
            metadata=FrogMetaData(**df_dict[CuratorConstants.METADATA_KEY]),
            objectives=FrogObjectives.from_df(df_dict[CuratorConstants.OBJECTIVE_KEY]),
            fva=FrogFVA.from_df(df_dict[CuratorConstants.FVA_KEY]),
            reaction_deletions=FrogReactionDeletions.from_df(
                df_dict[CuratorConstants.REACTIONDELETIONS_KEY]
            ),
            gene_deletions=FrogGeneDeletions.from_df(
                df_dict[CuratorConstants.GENEDELETIONS_KEY]
            ),
        )
        return report

    def add_to_omex(
        self, omex: Omex, location_prefix: str = f"./{FROG_PATH_PREFIX}/"
    ) -> None:
        """Add report to omex.

        :param omex: OMEX archive to add report to.
        :param location_prefix: prefix to where to write the FROG files in the OMEX
        """

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
