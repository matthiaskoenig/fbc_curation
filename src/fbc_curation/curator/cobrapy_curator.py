"""Provide cobrapy fbc curator."""

import logging
from pathlib import Path
from typing import Dict

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

from fbc_curation.constants import CuratorConstants
from fbc_curation.curator import Curator


logger = logging.getLogger(__file__)


class CuratorCobrapy(Curator):
    """FBC curator based on cobrapy."""

    def __init__(self, model_path: Path, objective_id: str = None):
        """Create instance."""
        super().__init__(model_path=model_path, objective_id=objective_id)

    def read_model(self) -> Model:
        """Read the model."""
        return read_sbml_model(str(self.model_path))

    def metadata(self) -> Dict:
        """Create metadata dictionary."""
        d = super().metadata()
        d["solver.name"] = f"cobrapy (glpk)"
        d["solver.version"] = f"{cobra_version}"
        return d

    def objective(self) -> pd.DataFrame:
        """Create pandas DataFrame with objective value.

        see https://cobrapy.readthedocs.io/en/latest/simulating.html
        """
        model = self.read_model()
        try:
            # fbc optimization
            solution = model.optimize()
            value = solution.objective_value
            status = CuratorConstants.STATUS_OPTIMAL
        except OptimizationError as e:
            logger.error(f"{e}")
            value = CuratorConstants.VALUE_INFEASIBLE
            status = CuratorConstants.STATUS_INFEASIBLE

        return pd.DataFrame(
            {
                "model": self.model_path.name,
                "objective": [self.objective_id],
                "status": [status],
                "value": [value],
            }
        )

    def fva(self) -> pd.DataFrame:
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
                    "model": self.model_path.name,
                    "objective": self.objective_id,
                    "reaction": df.index,
                    "flux": fluxes,
                    "status": CuratorConstants.STATUS_OPTIMAL,
                    "minimum": df.minimum,
                    "maximum": df.maximum,
                }
            )
        except OptimizationError as e:
            logger.error(f"{e}")
            df_out = pd.DataFrame(
                {
                    "model": self.model_path.name,
                    "objective": self.objective_id,
                    "reaction": [r.id for r in model.reactions],
                    "flux": fluxes,
                    "status": CuratorConstants.STATUS_INFEASIBLE,
                    "minimum": CuratorConstants.VALUE_INFEASIBLE,
                    "maximum": CuratorConstants.VALUE_INFEASIBLE,
                }
            )

        return df_out

    def gene_deletion(self) -> pd.DataFrame:
        """Create pd.DataFrame with results of gene deletion.

        https://cobrapy.readthedocs.io/en/latest/deletions.html
        :return: pandas.DataFrame
        """
        model = self.read_model()
        df = single_gene_deletion(model, model.genes)
        return pd.DataFrame(
            {
                "model": self.model_path.name,
                "objective": self.objective_id,
                "gene": [set(ids).pop() for ids in df.ids],
                "status": df.status,
                "value": df.growth,
            }
        )

    def reaction_deletion(self) -> pd.DataFrame:
        """Create pd.DataFramewith results of reaction deletion.

        https://cobrapy.readthedocs.io/en/latest/deletions.html
        :return: pandas.
        """
        model = self.read_model()
        df = single_reaction_deletion(model, model.reactions)
        return pd.DataFrame(
            {
                "model": self.model_path.name,
                "objective": self.objective_id,
                "reaction": [set(ids).pop() for ids in df.ids],
                "status": df.status,
                "value": df.growth,
            }
        )
