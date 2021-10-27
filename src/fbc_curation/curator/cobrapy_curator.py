"""Provide cobrapy fbc curator."""

from pathlib import Path
from typing import Dict

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
from pydantic import ValidationError
from pymetadata import log
from rich import print
from swiglpk import GLP_MAJOR_VERSION, GLP_MINOR_VERSION

from fbc_curation.curator import Curator
from fbc_curation.frog import (
    CuratorConstants,
    FrogFVA,
    FrogFVASingle,
    FrogGeneDeletion,
    FrogGeneDeletions,
    FrogMetaData,
    FrogObjective,
    FrogReactionDeletion,
    FrogReactionDeletions,
    StatusCode,
    Tool,
)


# use a single core
configuration = cobra.Configuration()
configuration.processes = 1

logger = log.get_logger(__name__)
logger.info(f"cobrapy processes: {configuration.processes}")


class CuratorCobrapy(Curator):
    """FBC curator based on cobrapy."""

    def __init__(self, model_path: Path, objective_id: str = None):
        """Create instance."""
        super().__init__(model_path=model_path, objective_id=objective_id)

    def read_model(self) -> Model:
        """Read the model."""
        return read_sbml_model(str(self.model_path), f_replace={})

    def metadata(self) -> FrogMetaData:
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

    def objective(self) -> FrogObjective:
        """Create pandas DataFrame with objective value.

        see https://cobrapy.readthedocs.io/en/latest/simulating.html
        """
        model = self.read_model()
        try:
            # fbc optimization
            solution = model.optimize()
            value = solution.objective_value
            status = StatusCode.OPTIMAL
        except OptimizationError as e:
            logger.error(f"{e}")
            value = CuratorConstants.VALUE_INFEASIBLE
            status = StatusCode.INFEASIBLE

        return FrogObjective(
            model=self.model_location,
            objective=self.objective_id,
            status=status,
            value=value,
        )

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
                    "status": CuratorConstants.STATUS_INFEASIBLE,
                    "minimum": CuratorConstants.VALUE_INFEASIBLE,
                    "maximum": CuratorConstants.VALUE_INFEASIBLE,
                    "fraction_optimum": 1.0,
                }
            )

        # Convert DataFrame to json
        fva = []
        for item in df_out.to_dict(orient="records"):
            try:
                fva.append(FrogFVASingle(**item))
            except ValidationError as e:
                print(item)
                print(e.json())

        return FrogFVA(fva=fva)

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

        json = df.to_dict(orient="records")
        deletions = []
        for item in json:
            try:
                deletions.append(FrogGeneDeletion(**item))
            except ValidationError as e:
                print(item)
                print(e.json())

        return FrogGeneDeletions(deletions=deletions)

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

        json = df.to_dict(orient="records")
        deletions = []
        for item in json:
            try:
                deletions.append(FrogReactionDeletion(**item))
            except ValidationError as e:
                print(item)
                print(e.json())

        return FrogReactionDeletions(deletions=deletions)
