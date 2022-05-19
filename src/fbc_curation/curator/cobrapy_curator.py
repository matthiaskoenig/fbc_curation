"""Provide cobrapy fbc curator."""

from pathlib import Path
from typing import List

import cobra
import pandas as pd
from cobra import __version__ as cobra_version
from cobra.core import Model
from cobra.exceptions import OptimizationError
from cobra.flux_analysis import (
    flux_variability_analysis,
    single_gene_deletion,
    single_reaction_deletion,
)
from cobra.io import read_sbml_model
from pymetadata import log
from swiglpk import GLP_MAJOR_VERSION, GLP_MINOR_VERSION

from fbc_curation.curator import Curator
from fbc_curation.frog import (
    Creator,
    CuratorConstants,
    FrogFVA,
    FrogGeneDeletions,
    FrogMetaData,
    FrogObjectives,
    FrogReactionDeletions,
    StatusCode,
    Tool,
)


# use a single core
configuration = cobra.Configuration()
configuration.processes = 1

logger = log.get_logger(__name__)


class CuratorCobrapy(Curator):
    """FBC curator based on cobrapy."""

    def __init__(self, model_path: Path, frog_id: str, curators: List[Creator]):
        """Create instance."""
        Curator.__init__(
            self, model_path=model_path, frog_id=frog_id, curators=curators
        )

    def read_model(self) -> Model:
        """Read the model."""
        return read_sbml_model(str(self.model_path), f_replace={})

    def set_metadata(self) -> FrogMetaData:
        """Create metadata dictionary."""

        software = Tool(
            name="cobrapy",
            version=cobra_version,
            url="https://github.com/opencobra/cobrapy",
        )
        solver = Tool(
            name="glpk", version=f"{GLP_MAJOR_VERSION}.{GLP_MINOR_VERSION}", url=None
        )
        md = super().metadata(solver=solver, software=software)
        return md

    def objectives(self) -> FrogObjectives:
        """Create pandas DataFrame with objective value.

        see https://cobrapy.readthedocs.io/en/latest/simulating.html
        """
        model = self.read_model()
        try:
            solution = model.optimize()
            df = pd.DataFrame(
                {
                    "model": self.model_location,
                    "objective": self.objective_id,
                    "status": StatusCode.OPTIMAL,
                    "value": solution.objective_value,
                },
                index=[0],
            )
        except Exception:
            df = pd.DataFrame(
                {
                    "model": self.model_location,
                    "objective": self.objective_id,
                    "status": StatusCode.INFEASIBLE,
                    "value": CuratorConstants.VALUE_INFEASIBLE,
                },
                index=[0],
            )
        return FrogObjectives.from_df(df)

    def fva(self) -> FrogFVA:
        """Create DataFrame file with minimum and maximum value of FVA.

        Runs flux variability analysis.
        see https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA
        """
        model = self.read_model()
        solution = model.optimize()
        fluxes = solution.fluxes
        try:
            df = flux_variability_analysis(
                model, model.reactions, fraction_of_optimum=1.0
            )
            df_out = pd.DataFrame(
                {
                    "model": self.model_location,
                    "objective": self.objective_id,
                    "reaction": df.index,
                    "flux": fluxes,
                    "status": StatusCode.OPTIMAL,
                    "minimum": df.minimum,
                    "maximum": df.maximum,
                    "fraction_optimum": 1.0,
                }
            )
        except OptimizationError as e:
            logger.error(f"{e}")
            df_out = pd.DataFrame(
                {
                    "model": self.model_location,
                    "objective": self.objective_id,
                    "reaction": [r.id for r in model.reactions],
                    "flux": fluxes,
                    "status": StatusCode.INFEASIBLE,
                    "minimum": CuratorConstants.VALUE_INFEASIBLE,
                    "maximum": CuratorConstants.VALUE_INFEASIBLE,
                    "fraction_optimum": 1.0,
                }
            )
        return FrogFVA.from_df(df_out)

    def gene_deletions(self) -> FrogGeneDeletions:
        """Create pd.DataFrame with results of gene deletion.

        https://cobrapy.readthedocs.io/en/latest/deletions.html
        :return: pandas.DataFrame
        """
        model = self.read_model()
        df = single_gene_deletion(model, model.genes)
        df = pd.DataFrame(
            {
                "model": self.model_location,
                "objective": self.objective_id,
                "gene": [set(ids).pop() for ids in df.ids],
                "status": df.status,
                "value": df.growth,
            }
        )
        df.loc[
            df.status == StatusCode.INFEASIBLE, "value"
        ] = CuratorConstants.VALUE_INFEASIBLE

        if not model.genes:
            logger.error("no genes in model")
            df = pd.DataFrame(
                columns=[
                    "model",
                    "objective",
                    "gene",
                    "status",
                    "value",
                ]
            )

        return FrogGeneDeletions.from_df(df)

    def reaction_deletions(self) -> FrogReactionDeletions:
        """Create pd.DataFrame with results of reaction deletion.

        https://cobrapy.readthedocs.io/en/latest/deletions.html
        :return: pandas.
        """
        model = self.read_model()
        df = single_reaction_deletion(model, model.reactions)

        df = pd.DataFrame(
            {
                "model": self.model_location,
                "objective": self.objective_id,
                "reaction": [set(ids).pop() for ids in df.ids],
                "status": df.status,
                "value": df.growth,
            }
        )
        df.loc[
            df.status == StatusCode.INFEASIBLE, "value"
        ] = CuratorConstants.VALUE_INFEASIBLE

        return FrogReactionDeletions.from_df(df)
