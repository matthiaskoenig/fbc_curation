"""Curate fbc with cameo."""

from pathlib import Path
from typing import Dict

import pandas as pd
from cameo import __version__ as cameo_version
from cameo import fba
from cameo.flux_analysis.analysis import (
    FluxVariabilityResult,
    flux_variability_analysis,
)
from cobra.core import Model
from cobra.io import read_sbml_model
from pymetadata import log
from swiglpk import GLP_MAJOR_VERSION, GLP_MINOR_VERSION

from fbc_curation.frog import CuratorConstants, FrogMetaData, Tool, StatusCode, \
    FrogReactionDeletions, FrogGeneDeletions, FrogFVA, FrogObjective, SId
from fbc_curation.curator import Curator


logger = log.get_logger(__name__)


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
        """Create instance."""
        Curator.__init__(self, model_path=model_path, objective_id=objective_id)

    def read_model(self) -> Model:
        return read_sbml_model(str(self.model_path), f_replace={})

    def metadata(self) -> FrogMetaData:
        """Create metadata dictionary."""
        software = Tool(
            name="cameo",
            version=cameo_version,
            url="https://github.com/opencobra/cobrapy",
        )
        solver = Tool(
            name="glpk", version=f"{GLP_MAJOR_VERSION}.{GLP_MINOR_VERSION}",
            url=None
        )
        return super().metadata(software=software, solver=solver)

    def objective(self) -> FrogObjective:
        model = self.read_model()
        try:
            # fbc optimization
            result = fba(model)
            value = result.objective_value
            status = StatusCode.OPTIMAL
        except Exception as e:
            logger.error(f"{e}")
            value = CuratorConstants.VALUE_INFEASIBLE
            status = StatusCode.INFEASIBLE

        return FrogObjective(
            model=SId(sid=self.model_path.name),
            objective=SId(sid=self.objective_id),
            status=status,
            value=value,
        )

    def fva(self) -> FrogFVA:
        model = self.read_model()
        result = fba(model)
        fluxes = result.fluxes
        try:
            fva_result = flux_variability_analysis(
                model, reactions=model.reactions, fraction_of_optimum=1.0
            )  # type: FluxVariabilityResult
            df = fva_result.data_frame
            df_out = pd.DataFrame(
                {
                    "model": self.model_path.name,
                    "objective": self.objective_id,
                    "reaction": df.index,
                    "flux": fluxes,
                    "status": StatusCode.OPTIMAL,
                    "minimum": df.lower_bound,
                    "maximum": df.upper_bound,
                    "fraction_optimum": 1.0,
                }
            )
        except Exception as e:
            logger.error(f"{e}")
            df_out = pd.DataFrame(
                {
                    "model": self.model_path.name,
                    "objective": self.objective_id,
                    "reaction": [r.id for r in model.reactions],
                    "flux": fluxes,
                    "status": StatusCode.INFEASIBLE,
                    "minimum": CuratorConstants.VALUE_INFEASIBLE,
                    "maximum": CuratorConstants.VALUE_INFEASIBLE,
                    "fraction_optimum": 1.0,
                }
            )

        json = df_out.to_dict()
        return FrogFVA(**json)

    def gene_deletions(self) -> FrogGeneDeletions:
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
                status = StatusCode.OPTIMAL
            except Exception as e:
                logger.error(f"{e}")
                value = CuratorConstants.VALUE_INFEASIBLE
                status = StatusCode.INFEASIBLE
            gene_status.append(status)
            gene_values.append(value)

            # restore bounds
            for rid, bounds in reaction_bounds.items():
                model.reactions.get_by_id(rid).bounds = bounds[:]

        df = pd.DataFrame(
            {
                "model": self.model_path.name,
                "objective": self.objective_id,
                "gene": [gene.id for gene in model.genes],
                "status": gene_status,
                "value": gene_values,
            }
        )
        json = df.to_dict()
        return FrogGeneDeletions(**json)

    def reaction_deletion(self) -> FrogReactionDeletions:
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
                status = StatusCode.OPTIMAL
            except Exception as e:
                logger.error(f"{e}")
                value = CuratorConstants.VALUE_INFEASIBLE
                status = StatusCode.STATUS_INFEASIBLE

            reaction_status.append(status)
            reaction_values.append(value)

            # restore bounds
            reaction.bounds = reaction_bounds[:]

        df = pd.DataFrame(
            {
                "model": self.model_path.name,
                "objective": self.objective_id,
                "reaction": [r.id for r in model.reactions],
                "status": reaction_status,
                "value": reaction_values,
            }
        )

        json = df.to_dict()
        return FrogReactionDeletions(**json)
