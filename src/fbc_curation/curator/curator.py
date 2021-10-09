"""Base class for all FBC curators."""
from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Dict, List

import cobra
import libsbml
import pandas as pd
from cobra.io import read_sbml_model
from pymetadata import log
from pymetadata.console import console

from fbc_curation.curator.metadata import create_metadata
from fbc_curation.curator.results import CuratorResults


ObjectiveInformation = namedtuple(
    "ObjectiveInformation", "active_objective objective_ids"
)

logger = log.get_logger(__name__)


class Curator:
    """Base class of all Curator implementations."""

    def __init__(self, model_path: Path, objective_id: str = None):
        """Create instance."""
        if not model_path.exists():
            raise ValueError(f"model_path does not exist: '{model_path}'")

        self.model_path = model_path
        self.active_objective, self.objective_ids = Curator.read_objective_information(
            model_path
        )

        if objective_id is None:
            logger.warning(
                f"No objective id provided, using the active objective: "
                f"{self.active_objective}"
            )
            self.objective_id = self.active_objective
        else:
            if objective_id not in self.objective_ids:
                logger.error(
                    f"objective id does not exist in model: '{self.objective_id}', "
                    f"using the active objective: {self.active_objective}"
                )
                self.objective_id = self.active_objective
            else:
                self.objective_id = objective_id

    def __str__(self):
        """Create string representation."""
        lines = [
            f"--- {self.__class__.__name__} ---",
            f"\tmodel_path: {self.model_path}",
            f"\tobjective_id: {self.objective_id}",
        ]
        return "\n".join(lines)

    def read_model(self):
        raise NotImplementedError

    def metadata(self) -> Dict:
        return create_metadata(path=self.model_path)

    def objective(self) -> pd.DataFrame:
        raise NotImplementedError

    def fva(self) -> pd.DataFrame:
        raise NotImplementedError

    def gene_deletion(self) -> pd.DataFrame:
        raise NotImplementedError

    def reaction_deletion(self) -> pd.DataFrame:
        raise NotImplementedError

    def run(self) -> CuratorResults:
        """Run the curator and stores the results."""

        console.rule("CuratorResults", style="white")
        self._print_header(f"{self.__class__.__name__}: metadata")
        metadata = self.metadata()

        self._print_header(f"{self.__class__.__name__}: objective")
        objective = self.objective()

        self._print_header(f"{self.__class__.__name__}: fva")
        fva = self.fva()

        self._print_header(f"{self.__class__.__name__}: gene_deletion")
        gene_deletion = self.gene_deletion()

        self._print_header(f"{self.__class__.__name__}: reaction_deletion")
        reaction_deletion = self.reaction_deletion()

        return CuratorResults(
            metadata=metadata,
            objective_id=self.objective_id,
            objective=objective,
            fva=fva,
            gene_deletion=gene_deletion,
            reaction_deletion=reaction_deletion,
        )

    @staticmethod
    def _print_header(title):
        console.print(f"* {title}")

    @staticmethod
    def knockout_reactions_for_genes(
        model_path: Path, genes=None
    ) -> Dict[str, List[str]]:
        """Calculate mapping of genes to affected reactions.

        Which reactions are knocked out by a given gene.
        A single gene knockout can affect multiple reactions.
        Uses GPR mappings.
        """
        model = read_sbml_model(str(model_path), f_replace={})  # type: cobra.core.Model
        if genes is None:
            genes = model.genes

        knockout_reactions = defaultdict(list)
        for reaction in model.reactions:  # type: cobra.core.Reaction
            gpr = reaction.gene_reaction_rule
            tree, gpr_genes = cobra.core.gene.parse_gpr(gpr)
            for gene in genes:  # type: cobra.core.Gene
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
    def read_objective_information(model_path: Path) -> ObjectiveInformation:
        """Read objective information from SBML file structure."""
        # read objective information from sbml (multiple objectives)
        doc = libsbml.readSBMLFromFile(str(model_path))  # type: libsbml.SBMLDocument
        model = doc.getModel()  # type: libsbml.Model
        fbc_model = model.getPlugin("fbc")  # type: libsbml.FbcModelPlugin
        if fbc_model is None:
            # model is an old SBML model without fbc information (use cobra default)
            # problems with the automatic up-conversions
            active_objective = "obj"
            objective_ids = ["obj"]
        else:
            active_objective = fbc_model.getActiveObjective().getId()
            objective_ids = []
            for objective in fbc_model.getListOfObjectives():  # type: libsbml.Objective
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


if __name__ == "__main__":
    from fbc_curation import EXAMPLE_PATH

    model_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"
    Curator.knockout_reactions_for_genes(model_path=model_path)
