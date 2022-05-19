"""Base class for all FBC curators."""
import os
import platform
from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Dict, List, Optional

import cobra
import libsbml
from cobra.io import read_sbml_model
from pymetadata import log
from pymetadata.console import console

from fbc_curation import __citation__, __software__, __version__
from fbc_curation.frog import (
    Creator,
    FrogFVA,
    FrogGeneDeletions,
    FrogMetaData,
    FrogObjectives,
    FrogReactionDeletions,
    FrogReport,
    Tool,
)


ObjectiveInformation = namedtuple(
    "ObjectiveInformation", "active_objective objective_ids"
)

logger = log.get_logger(__name__)


class Curator:
    """Base class of all Curator implementations."""

    def __init__(self, model_path: Path, frog_id: str, curators: List[Creator]):
        """Create instance."""
        if not model_path.exists():
            raise ValueError(f"model_path does not exist: '{model_path}'")

        self.frog_id: str = frog_id
        self.curators = curators
        self.model_path: Path = model_path
        self.model_location: str = f"./{self.model_path.name}"
        active_objective, objective_ids = Curator._read_objective_information(
            model_path
        )
        self.objective_id = active_objective

    def __str__(self) -> str:
        """Create string representation."""
        lines = [
            f"--- {self.__class__.__name__} ---",
            f"\tmodel_path: {self.model_path}",
            f"\tobjective_id: {self.objective_id}",
        ]
        return "\n".join(lines)

    def read_model(self) -> None:
        """Read the model."""
        raise NotImplementedError

    def metadata(self, software: Tool, solver: Tool) -> FrogMetaData:
        """Create metadata."""
        md = FrogMetaData(
            model_location=self.model_location,
            model_md5=FrogMetaData.md5_for_path(self.model_path),
            frog_id=self.frog_id,
            frog_software=Tool(
                name=__software__,
                version=__version__,
                url=__citation__,
            ),
            curators=self.curators,
            software=software,
            solver=solver,
            environment=f"{os.name}, {platform.system()}, {platform.release()}",
        )

        return md

    def set_metadata(self) -> FrogMetaData:
        """Create metadata for given curator."""
        pass

    def objectives(self) -> FrogObjectives:
        """Perform objectives."""
        raise NotImplementedError

    def fva(self) -> FrogFVA:
        """Perform FVA."""
        raise NotImplementedError

    def gene_deletions(self) -> FrogGeneDeletions:
        """Perform gene deletions."""
        raise NotImplementedError

    def reaction_deletions(self) -> FrogReactionDeletions:
        """Perform reaction deletions."""
        raise NotImplementedError

    def run(self) -> FrogReport:
        """Run the curator and return the FROG report."""

        console.rule(f"FROG {self.__class__.__name__}", style="white")
        logger.info("* metadata")
        metadata = self.set_metadata()

        logger.info("* objectives")
        objectives = self.objectives()

        logger.info("* fva")
        fva = self.fva()

        logger.info("* reactiondeletions")
        reaction_deletions = self.reaction_deletions()

        logger.info("* genedeletions")
        gene_deletions = self.gene_deletions()

        return FrogReport(
            metadata=metadata,
            objectives=objectives,
            fva=fva,
            gene_deletions=gene_deletions,
            reaction_deletions=reaction_deletions,
        )

    @staticmethod
    def _knockout_reactions_for_genes(
        model_path: Path, genes: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """Calculate mapping of genes to affected reactions.

        Which reactions are knocked out by a given gene.
        A single gene knockout can affect multiple reactions.
        Uses GPR mappings.
        """
        model: cobra.core.Model = read_sbml_model(str(model_path), f_replace={})
        if genes is None:
            genes = model.genes

        knockout_reactions = defaultdict(list)
        for reaction in model.reactions:  # type: cobra.core.Reaction
            gpr = reaction.gene_reaction_rule
            tree, gpr_genes = cobra.core.gene.parse_gpr(gpr)
            gene: cobra.core.Gene
            for gene in genes:
                if gene.id not in gpr_genes:
                    gene_essential = False
                else:
                    # eval_gpr: True if the gene reaction rule is true with
                    # the given knockouts otherwise false
                    gene_essential = not cobra.core.gene.eval_gpr(
                        tree, knockouts={gene.id}
                    )
                if gene_essential:
                    knockout_reactions[gene.id].append(reaction.id)

        return knockout_reactions

    @staticmethod
    def _read_objective_information(model_path: Path) -> ObjectiveInformation:
        """Read objective information from SBML file structure."""
        # read objective information from sbml (multiple objectives)
        doc = libsbml.SBMLDocument = libsbml.readSBMLFromFile(str(model_path))
        model: libsbml.Model = doc.getModel()
        fbc_model: libsbml.FbcModelPlugin = model.getPlugin("fbc")
        if fbc_model is None:
            # model is an old SBML model without fbc information (use cobra default)
            # problems with the automatic up-conversions
            active_objective = "obj"
            objective_ids = ["obj"]
        else:
            active_objective = fbc_model.getActiveObjective().getId()
            objective_ids = []
            objective: libsbml.Objective
            for objective in fbc_model.getListOfObjectives():
                objective_ids.append(objective.getId())

        if len(objective_ids) > 1:
            logger.warning(
                f"Multiple objectives exist in SBML-fbc ({objective_ids}), "
                f"only active objective '{active_objective}' results "
                f"are reported"
            )
        return ObjectiveInformation(
            active_objective=active_objective, objective_ids=objective_ids
        )
