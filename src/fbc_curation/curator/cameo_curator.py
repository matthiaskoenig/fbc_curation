import logging
from pathlib import Path

import pandas as pd
from cameo import fba, load_model
from cameo.flux_analysis.analysis import (
    FluxVariabilityResult,
    flux_variability_analysis,
)
from cobra.core import Gene, Model, Reaction

from fbc_curation.constants import CuratorConstants
from fbc_curation.curator import Curator


logger = logging.getLogger(__name__)


class CuratorCameo(Curator):
    """FBC curator based on cameo.

    Cameo is a high-level python library developed to aid the strain design
    process in metabolic engineering projects. The library provides a modular
    framework of simulation and strain design methods that targets developers
    that want to develop new design algorithms and custom analysis workflows.
    Furthermore, it exposes a high-level API to users that just want to
    compute promising strain designs.

    https://pythonhosted.org/cameo/
    """

    def __init__(self, model_path: Path, objective_id: str = None):
        Curator.__init__(self, model_path=model_path, objective_id=objective_id)

    def read_model(self) -> Model:
        return load_model(str(self.model_path), sanitize=False)

    def objective(self) -> pd.DataFrame:
        model = self.read_model()
        try:
            # fbc optimization
            result = fba(model)
            value = result.objective_value
            status = CuratorConstants.STATUS_OPTIMAL
        except Exception as e:
            logger.error(f"{e}")
            value = CuratorConstants.VALUE_INFEASIBLE
            status = CuratorConstants.STATUS_INFEASIBLE

        return pd.DataFrame(
            {
                "model": model.id,
                "objective": [self.objective_id],
                "status": [status],
                "value": [value],
            }
        )

    def fva(self) -> pd.DataFrame:
        model = self.read_model()
        try:
            fva_result = flux_variability_analysis(
                model, reactions=model.reactions, fraction_of_optimum=1.0
            )  # type: FluxVariabilityResult
            df = fva_result.data_frame
            df_out = pd.DataFrame(
                {
                    "model": model.id,
                    "objective": self.objective_id,
                    "reaction": df.index,
                    "status": CuratorConstants.STATUS_OPTIMAL,
                    "minimum": df.lower_bound,
                    "maximum": df.upper_bound,
                }
            )
        except Exception as e:
            logger.error(f"{e}")
            df_out = pd.DataFrame(
                {
                    "model": model.id,
                    "objective": self.objective_id,
                    "reaction": [r.id for r in model.reactions],
                    "status": CuratorConstants.STATUS_INFEASIBLE,
                    "minimum": CuratorConstants.VALUE_INFEASIBLE,
                    "maximum": CuratorConstants.VALUE_INFEASIBLE,
                }
            )
        return df_out

    def gene_deletion(self) -> pd.DataFrame:
        model = self.read_model()
        gene_status = []
        gene_values = []

        knockout_reactions = self.knockout_reactions_for_genes(self.model_path)

        for gene in model.genes:
            reaction_bounds = dict()
            # knockout all reactions affected by gene by setting bounds zero
            for rid in knockout_reactions[gene.id]:
                reaction = model.reactions.get_by_id(rid)
                reaction_bounds[reaction.id] = (
                    reaction.lower_bound,
                    reaction.upper_bound,
                )
                reaction.bounds = (0, 0)
            try:
                # run fba
                result = fba(model)
                value = result.objective_value
                status = CuratorConstants.STATUS_OPTIMAL
            except Exception as e:
                logger.error(f"{e}")
                value = CuratorConstants.VALUE_INFEASIBLE
                status = CuratorConstants.STATUS_INFEASIBLE
            gene_status.append(status)
            gene_values.append(value)

            # restore bounds
            for rid, bounds in reaction_bounds.items():
                model.reactions.get_by_id(rid).bounds = bounds[:]

        return pd.DataFrame(
            {
                "model": model.id,
                "objective": self.objective_id,
                "gene": [gene.id for gene in model.genes],
                "status": gene_status,
                "value": gene_values,
            }
        )

    def reaction_deletion(self) -> pd.DataFrame:
        model = self.read_model()
        reaction_status = []
        reaction_values = []

        for reaction in model.reactions:
            reaction_bounds = (reaction.lower_bound, reaction.upper_bound)
            reaction.bounds = (0, 0)

            # run fba
            try:
                result = fba(model)
                value = result.objective_value
                status = CuratorConstants.STATUS_OPTIMAL
            except Exception as e:
                logger.error(f"{e}")
                value = CuratorConstants.VALUE_INFEASIBLE
                status = CuratorConstants.STATUS_INFEASIBLE

            reaction_status.append(status)
            reaction_values.append(value)

            # restore bounds
            reaction.bounds = reaction_bounds[:]

        return pd.DataFrame(
            {
                "model": model.id,
                "objective": self.objective_id,
                "reaction": [r.id for r in model.reactions],
                "status": reaction_status,
                "value": reaction_values,
            }
        )
