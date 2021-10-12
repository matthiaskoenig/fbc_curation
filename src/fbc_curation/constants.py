"""Reused constants."""
from typing import List

from fbc_curation.metadata import FrogMetaData

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


class CuratorConstants:
    """Class storing constants for curation and file format."""

    # keys of outputs
    METADATA_KEY = "metadata"
    OBJECTIVE_KEY = "objective"
    FVA_KEY = "fva"
    GENE_DELETION_KEY = "gene_deletion"
    REACTION_DELETION_KEY = "reaction_deletion"
    KEYS = [
        OBJECTIVE_KEY,
        FVA_KEY,
        GENE_DELETION_KEY,
        REACTION_DELETION_KEY,
    ]

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
    OBJECTIVE_FIELDS = ["model", "objective", "status", "value"]
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

    # status codes
    STATUS_OPTIMAL = "optimal"
    STATUS_INFEASIBLE = "infeasible"
    STATUS_CODES = [STATUS_OPTIMAL, STATUS_INFEASIBLE]

    # special settings for comparison
    VALUE_INFEASIBLE = ""  # pd.NA
    NUM_DECIMALS = 6  # decimals to write in the solution


if __name__ == "__main__":
    console.print(Frog.schema_json(indent=2))
