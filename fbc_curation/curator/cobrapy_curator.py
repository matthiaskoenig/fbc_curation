from typing import List, Dict
import logging
from pathlib import Path
import pandas as pd

import cobra
from cobra.io import read_sbml_model
from cobra.core import Model
from cobra.exceptions import OptimizationError
from cobra.flux_analysis import flux_variability_analysis
from cobra.flux_analysis import single_gene_deletion, single_reaction_deletion

from fbc_curation.curator import Curator, CuratorConstants

logger = logging.getLogger(__file__)


class CuratorCobrapy(Curator):
    """ FBC curator based on cameo.

    Uses GLPK as default solver.
    """

    def __init__(self, model_path: Path, objective_id: str = None):
        Curator.__init__(self, model_path=model_path, objective_id=objective_id)

    def read_model(self) -> Model:
        return read_sbml_model(str(self.model_path))  # type: cobra.Model

    def objective(self) -> pd.DataFrame:
        """ Creates pandas DataFrame with objective value.

        see https://cobrapy.readthedocs.io/en/latest/simulating.html

        :return:
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
                "model": model.id,
                "objective": [self.objective_id],
                "status": [status],
                "value": [value],
             })

    def fva(self) -> pd.DataFrame:
        """ Creates DataFrame file with minimum and maximum value of Flux variability analysis.

        see https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA
        :return:
        """
        model = self.read_model()
        try:
            df = flux_variability_analysis(model, model.reactions, fraction_of_optimum=1.0)
            print(df.head())
            df_out = pd.DataFrame(
                {
                    "model": model.id,
                    "objective": self.objective_id,
                    "reaction": df.index,
                    "status": CuratorConstants.STATUS_OPTIMAL,
                    "minimum": df.minimum,
                    "maximum": df.maximum
                 })
        except OptimizationError as e:
            logger.error(f"{e}")
            df_out = pd.DataFrame(
                {
                    "model": model.id,
                    "objective": self.objective_id,
                    "reaction": [r.id for r in model.reactions],
                    "status": CuratorConstants.STATUS_INFEASIBLE,
                    "minimum": CuratorConstants.VALUE_INFEASIBLE,
                    "maximum": CuratorConstants.VALUE_INFEASIBLE,
                })

        return df_out

    def gene_deletion(self) -> pd.DataFrame:
        """ Create pd.DataFrame with results of gene deletion.

        https://cobrapy.readthedocs.io/en/latest/deletions.html
        :return:
        """
        model = self.read_model()
        df = single_gene_deletion(model, model.genes)
        return pd.DataFrame(
            {
                "model": model.id,
                "objective": self.objective_id,
                "gene": [set(ids).pop() for ids in df.index],
                "status": df.status,
                "value": df.growth,
             })

    def reaction_deletion(self) -> pd.DataFrame:
        """ Create pd.DataFramewith results of reaction deletion.

        https://cobrapy.readthedocs.io/en/latest/deletions.html
        :return:
        """
        model = self.read_model()
        df = single_reaction_deletion(model, model.reactions)
        return pd.DataFrame(
            {
                "model": model.id,
                "objective": self.objective_id,
                "reaction": [set(ids).pop() for ids in df.index],
                "status": df.status,
                "value": df.growth,
             })
