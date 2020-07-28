"""
Base class for all FBC curators.
"""
import libsbml
from pathlib import Path
from typing import Dict, List
import pandas as pd
import logging

from .result import CuratorResults

logger = logging.getLogger(__name__)


class CuratorConstants:
    KEYS = ["objective", "fva", "gene_deletion", "reaction_deletion"]

    # default output filenames
    FILENAME_OBJECTIVE_FILE = "01_objective.tsv"
    FILENAME_FVA_FILE = "02_fva.tsv"
    FILENAME_GENE_DELETION_FILE = "03_gene_deletion.tsv"
    FILENAME_REACTION_DELETION_FILE = "04_reaction_deletion.tsv"

    NUM_DECIMALS = 6  # decimals to write in the solution

    STATUS_OPTIMAL = "optimal"
    STATUS_INFEASIBLE = "infeasible"
    VALUE_INFEASIBLE = ''

    OBJECTIVE_VALUE_COLUMNS = ["model", "objective", "status", "value"]
    FVA_COLUMNS = ["model", "objective", "reaction", "status", "minimum", "maximum"]
    GENE_DELETIONS_COLUMNS = ["model", "objective", "gene", "status", "value"]
    REACTION_DELETION_COLUMNS = ["model", "objective", "reaction", "status", "value"]


class Curator:
    """
    Base class of all Curator implementations.
    """
    def __init__(self, model_path: Path, objective_id: str = None):
        if not model_path.exists():
            raise ValueError(f"model_path does not exist: '{model_path}'")

        self.model_path = model_path
        self.active_objective, self.objective_ids = Curator.read_objective_information(model_path)

        if objective_id is None:
            logger.warning(f"No objective id provided, using the active objective: {self.active_objective}")
            self.objective_id = self.active_objective
        else:
            if objective_id not in self.objective_ids:
                logger.error(f"objective id does not exist in model: '{self.objective_id}', "
                             f"using the active objective: {self.active_objective}")
                self.objective_id = self.active_objective
            else:
                self.objective_id = objective_id

    def __str__(self):
        lines = [
            f"--- {self.__class__.__name__} ---",
            f"\tmodel_path: {self.model_path}",
            f"\tobjective_id: {self.objective_id}",
        ]
        return "\n".join(lines)

    def read_model(self):
        raise NotImplementedError

    def objective(self) -> pd.DataFrame:
        raise NotImplementedError

    def fva(self) -> pd.DataFrame:
        raise NotImplementedError

    def gene_deletion(self) -> pd.DataFrame:
        raise NotImplementedError

    def reaction_deletion(self) -> pd.DataFrame:
        raise NotImplementedError

    def run(self, objective_id=None) -> CuratorResults:
        """Runs the curator and stores the results."""
        objective = self.objective()
        fva = self.fva()
        gene_deletion = self.gene_deletion()
        reaction_deletion = self.reaction_deletion()

        if objective_id is None:
            objective_id = self.active_objective

        return CuratorResults(
            objective_id=objective_id,
            objective=objective,
            fva=fva,
            gene_deletion=gene_deletion,
            reaction_deletion=reaction_deletion,
        )

    @staticmethod
    def _print_header(title):
        print()
        print("-" * 80)
        print(title)
        print("-" * 80)

    @staticmethod
    def read_objective_information(model_path) -> Dict:
        """ Reads objective information from SBML file structure

        :param model_path:
        :return:
        """
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
            logger.warning(f"Multiple objectives exist in SBML-fbc ({objective_ids}), "
                           f"only active objective '{active_objective}' results "
                           f"are reported")
        return {
            'active_objective': active_objective,
            'objective_ids': objective_ids
        }
