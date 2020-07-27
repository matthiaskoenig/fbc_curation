#!/bin/sh
"""
Module for creating FBC curation files via cobrapy.

Uses GLPK as default solver.
"""
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

from fbc_curation.fbc_curator import FBCCuratorImplementation, FBCCuratorResult

logger = logging.getLogger(__file__)


class FBCCuratorCobrapy(FBCCuratorImplementation):
    """Create FBC reference files with cobrapy."""

    def __init__(self, model_path: Path, objective_id: str = None):
        FBCCuratorImplementation.__init__(self, model_path=model_path, objective_id=objective_id)

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
            status = FBCCuratorResult.STATUS_OPTIMAL
        except OptimizationError as e:
            logger.error(f"{e}")
            value = FBCCuratorResult.VALUE_INFEASIBLE
            status = FBCCuratorResult.STATUS_INFEASIBLE

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
        # FIXME: ensure that correct values are returned and comparable
        try:
            df = flux_variability_analysis(model, model.reactions, fraction_of_optimum=1.0)
            print(df.head())
            df_out = pd.DataFrame(
                {
                    "model": model.id,
                    "objective": self.objective_id,
                    "reaction": df.index,
                    "status": FBCCuratorResult.STATUS_OPTIMAL,
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
                    "status": FBCCuratorResult.STATUS_INFEASIBLE,
                    "minimum": FBCCuratorResult.VALUE_INFEASIBLE,
                    "maximum": FBCCuratorResult.VALUE_INFEASIBLE,
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
