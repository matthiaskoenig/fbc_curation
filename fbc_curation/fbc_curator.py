"""
Base class for all FBC curators.
"""
import logging
from typing import Dict
import pandas as pd
from pathlib import Path
import libsbml

logger = logging.getLogger(__name__)


class FBCCuratorResult:
    KEYS = ["objective", "fva", "gene_deletion", "reaction_deletion"]

    # default output filenames
    FILENAME_OBJECTIVE_FILE = "01_objective.tsv"
    FILENAME_FVA_FILE = "02_fva.tsv"
    FILENAME_GENE_DELETION_FILE = "03_gene_deletion.tsv"
    FILENAME_REACTION_DELETION_FILE = "04_reaction_deletion.tsv"

    NUM_DECIMALS = 6  # decimals to write in the solution

    STATUS_OPTIMAL = "optimal"
    STATUS_INFEASIBLE = "infeasible"

    OBJECTIVE_VALUE_COLUMNS = ["model", "objective", "status", "value"]
    FVA_COLUMNS = ["model", "objective", "reaction", "status", "minimum", "maximum"]
    GENE_DELETIONS_COLUMNS = ["model", "objective", "gene", "status", "value"]
    REACTION_DELETION_COLUMNS = ["model", "objective", "reaction", "status", "value"]

    def __init__(self, objective_id: str, objective: pd.DataFrame, fva: pd.DataFrame,
                 gene_deletion: pd.DataFrame, reaction_deletion: pd.DataFrame,
                 num_decimals: int = None
                 ):
        self.objective_id = objective_id
        self.objective = objective
        self.fva = fva
        self.gene_deletion = gene_deletion
        self.reaction_deletion = reaction_deletion

        if not num_decimals:
            num_decimals = self.NUM_DECIMALS
        self.num_decimals = num_decimals

        # round and sort objective value
        for key in ["value"]:
            self.objective[key] = self.objective[key].apply(lambda x: round(x, self.num_decimals))
        self.objective.sort_values(by=['objective'], inplace=True)

        # round and sort fva
        for key in ["minimum", "maximum"]:
            self.fva[key] = self.fva[key].apply(lambda x: round(x, self.num_decimals))
        self.fva.sort_values(by=['reaction'], inplace=True)
        self.fva.index = range(len(self.fva))

        # round and sort gene_deletion
        for key in ["value"]:
            self.gene_deletion[key] = self.gene_deletion[key].apply(
                lambda x: round(x, self.num_decimals)).abs()  # abs fixes the -0.0 | +0.0 diffs
        self.gene_deletion.sort_values(by=['gene'], inplace=True)
        self.gene_deletion.index = range(len(self.gene_deletion))

        # round and sort reaction deletion
        for key in ["value"]:
            self.reaction_deletion[key] = self.reaction_deletion[key].apply(
                lambda x: round(x, self.num_decimals)).abs()  # abs fixes the -0.0 | +0.0 diffs
        self.reaction_deletion.sort_values(by=['reaction'], inplace=True)
        self.reaction_deletion.index = range(len(self.reaction_deletion))

    def write_results(self, path_out: Path):
        """Write results to path."""
        self.objective.to_csv(path_out / self.FILENAME_OBJECTIVE_FILE, sep="\t", index=False)
        self.fva.to_csv(path_out / self.FILENAME_FVA_FILE, sep="\t", index=False)
        self.reaction_deletion.to_csv(path_out / self.FILENAME_REACTION_DELETION_FILE, sep="\t", index=False)
        self.gene_deletion.to_csv(path_out / self.FILENAME_GENE_DELETION_FILE, sep="\t", index=False)

    def __eq__(self, other):
        """Compare results."""
        pass



    @classmethod
    def read_results(cls, path_in: Path):
        """Read fbc curation files from given directory."""
        path_objective = path_in / cls.FILENAME_OBJECTIVE_FILE
        path_fva = path_in / cls.FILENAME_FVA_FILE
        path_gene_deletion = path_in / cls.FILENAME_GENE_DELETION_FILE
        path_reaction_deletion = path_in / cls.FILENAME_REACTION_DELETION_FILE
        df_dict = dict()

        for k, path in enumerate([path_objective, path_fva, path_gene_deletion, path_reaction_deletion]):
            if not path_objective.exists():
                logger.error(f"Required file for fbc curation does not exist: '{path}'")
            else:
                df_dict[cls.KEYS[k]] = pd.read_csv(path, sep="\t", index=False)

        return FBCCuratorResult(**df_dict)




class FBCCuratorImplementation:

    def __init__(self, model_path: Path, objective_id: str=None):
        if not model_path.exists():
            raise ValueError(f"model_path does not exist: '{model_path}'")

        self.model_path = model_path

        self.objective_id = objective_id
        self.active_objective, self.objective_ids = FBCCuratorImplementation.read_objective_information(model_path)
        if self.objective_id not in self.objective_ids:
            logger.error(f"objective id does not exist in model:'{self.objective_id}'")

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

    def run(self, objective_id=None) -> FBCCuratorResult:
        """Runs the curator and stores the results."""
        objective_value = self.objective()
        fva = self.fva()
        gene_deletions = self.gene_deletions()
        reaction_deletions = self.reaction_deletions()

        if objective_id is None:
            objective_id = self.active_objective

        return FBCCuratorResult(
            objective_id=objective_id,
            objective_value=objective_value,
            fva=fva,
            gene_deletions=gene_deletions,
            reaction_deletions=reaction_deletions,
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
            logger.warnings(f"Multiple objectives exist in SBML-fbc ({objective_ids}), "
                            f"only active objective '{active_objective}' results "
                            f"are reported")
        return {
            'active_objective': active_objective,
            'objective_ids': objective_ids
        }
