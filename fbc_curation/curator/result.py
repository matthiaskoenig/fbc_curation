from pathlib import Path
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class CuratorResults:
    """
    Class for working with fbc curation results.
    CuratorResults can either be created by a Curator or read from file.
    """

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
            self.objective[key] = self.objective[key].apply(self._round)
        self.objective.sort_values(by=['objective'], inplace=True)

        # round and sort fva
        for key in ["minimum", "maximum"]:
            self.fva[key] = self.fva[key].apply(self._round)
        self.fva.sort_values(by=['reaction'], inplace=True)
        self.fva.index = range(len(self.fva))

        # round and sort gene_deletion
        for key in ["value"]:
            self.gene_deletion[key] = self.gene_deletion[key].apply(self._round)
        self.gene_deletion.sort_values(by=['gene'], inplace=True)
        self.gene_deletion.index = range(len(self.gene_deletion))

        # round and sort reaction deletion
        for key in ["value"]:
            self.reaction_deletion[key] = self.reaction_deletion[key].apply(self._round)
        self.reaction_deletion.sort_values(by=['reaction'], inplace=True)
        self.reaction_deletion.index = range(len(self.reaction_deletion))

    def _round(self, x):
        if x == CuratorResults.VALUE_INFEASIBLE:
            return x
        else:
            # FIXME: this creates a bug for negative values
            return abs(round(x, self.num_decimals))  # abs fixes the -0.0 | +0.0 diffs

    def write_results(self, path_out: Path):
        """Write results to path."""
        if not path_out.exists():
            logger.warning(f"Creating results path: {path_out}")
            path_out.mkdir(parents=True)

        self.objective.to_csv(path_out / self.FILENAME_OBJECTIVE_FILE, sep="\t", index=False)
        self.fva.to_csv(path_out / self.FILENAME_FVA_FILE, sep="\t", index=False)
        self.reaction_deletion.to_csv(path_out / self.FILENAME_REACTION_DELETION_FILE, sep="\t", index=False)
        self.gene_deletion.to_csv(path_out / self.FILENAME_GENE_DELETION_FILE, sep="\t", index=False)

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
                df_dict[cls.KEYS[k]] = pd.read_csv(path, sep="\t")

        objective_id = df_dict['objective'].objective.values[0]

        return CuratorResults(objective_id=objective_id, **df_dict)

    def __eq__(self, other):
        """Compare results."""
        pass
        # FIXME: implement

    def validate(self):
        pass
    # FIXME: implement



