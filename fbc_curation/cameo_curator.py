
import logging
import pandas as pd
from pathlib import Path
from cobra.core import Reaction, Gene, Model

from cameo import load_model, fba
from cameo.flux_analysis.analysis import flux_variability_analysis, FluxVariabilityResult

from fbc_curation.fbc_curator import FBCCuratorImplementation, FBCCuratorResult

logger = logging.getLogger(__name__)


class FBCCuratorCameo(FBCCuratorImplementation):
    """ FBC curator based on cameo.

    Cameo is a high-level python library developed to aid the strain design
    process in metabolic engineering projects. The library provides a modular
    framework of simulation and strain design methods that targets developers
    that want to develop new design algorithms and custom analysis workflows.
    Furthermore, it exposes a high-level API to users that just want to
    compute promising strain designs.

    https://pythonhosted.org/cameo/
    """

    def __init__(self, model_path: Path, objective_id: str = None):
        FBCCuratorImplementation.__init__(self, model_path=model_path, objective_id=objective_id)

    def read_model(self):
        return load_model(str(self.model_path))  # type: Model

    def objective(self) -> pd.DataFrame:
        model = self.read_model()
        try:
            # fbc optimization
            result = fba(model)
            value = result.objective_value
            status = FBCCuratorResult.STATUS_OPTIMAL
        except Exception as e:
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
        model = self.read_model()
        try:
            fva_result = flux_variability_analysis(model, reactions=model.reactions)  # type: FluxVariabilityResult
            df = fva_result.data_frame
            df_out = pd.DataFrame(
                {
                    "model": model.id,
                    "objective": self.objective_id,
                    "reaction": df.index,
                    "status": FBCCuratorResult.STATUS_OPTIMAL,
                    "minimum": df.lower_bound,
                    "maximum": df.upper_bound
                 })
        except Exception as e:
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
        model = self.read_model()
        gene_status = []
        gene_values = []
        for gene in model.genes:
            reaction_bounds = dict()
            # knockout all reactions for gene by setting bounds zero
            for reaction in gene.reactions:
                if reaction.functional:
                    reaction_bounds[reaction.id] = (reaction.lower_bound, reaction.upper_bound)
                    reaction.bounds = (0, 0)

            # run fba
            try:
                result = fba(model)
                value = result.objective_value
                status = FBCCuratorResult.STATUS_OPTIMAL
            except Exception as e:
                logger.error(f"{e}")
                value = FBCCuratorResult.VALUE_INFEASIBLE
                status = FBCCuratorResult.STATUS_INFEASIBLE
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
             })

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
                status = FBCCuratorResult.STATUS_OPTIMAL
            except Exception as e:
                logger.error(f"{e}")
                value = FBCCuratorResult.VALUE_INFEASIBLE
                status = FBCCuratorResult.STATUS_INFEASIBLE

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
             })
