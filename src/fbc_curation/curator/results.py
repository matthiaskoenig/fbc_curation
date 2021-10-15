"""Manage FBC curation results."""
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from pydantic import BaseModel
from pymetadata import log
from pymetadata.console import console

from fbc_curation.frog import CuratorConstants, FrogReport


logger = log.get_logger(__name__)


# FIXME: use pydantic model here with JSON
class FROGResults:
    """Class for working with fbc curation results.

    CuratorResults can either be created by a Curator or read from file.
    """

    def __init__(
        self,
        metadata: dict,
        objective_id: str,
        objective: pd.DataFrame,
        fva: pd.DataFrame,
        gene_deletion: pd.DataFrame,
        reaction_deletion: pd.DataFrame,
        num_decimals: int = None,
    ):
        """Create instance."""
        self.metadata = metadata
        self.objective_id = objective_id
        self.objective = objective
        self.fva = fva
        self.gene_deletion = gene_deletion
        self.reaction_deletion = reaction_deletion

        if not num_decimals:
            num_decimals = CuratorConstants.NUM_DECIMALS
        self.num_decimals = num_decimals

        # FIXME: processing must be done on creating the files ?!
        # round and sort objective value
        for key in ["value"]:
            self.objective[key] = self.objective[key].apply(self._round)
        self.objective.sort_values(by=["objective"], inplace=True)

        # round and sort fva
        for key in ["flux", "minimum", "maximum"]:
            self.fva[key] = self.fva[key].apply(self._round)
        self.fva.sort_values(by=["reaction"], inplace=True)
        self.fva.index = range(len(self.fva))

        # round and sort gene_deletion
        for key in ["value"]:
            self.gene_deletion[key] = self.gene_deletion[key].apply(self._round)
        self.gene_deletion.sort_values(by=["gene"], inplace=True)
        self.gene_deletion.index = range(len(self.gene_deletion))

        # round and sort reaction deletion
        for key in ["value"]:
            self.reaction_deletion[key] = self.reaction_deletion[key].apply(self._round)
        self.reaction_deletion.sort_values(by=["reaction"], inplace=True)
        self.reaction_deletion.index = range(len(self.reaction_deletion))

        # validate
        self.validate()

    def _round(self, x):
        """Round the float and sets small values positive.

        Ensuring positivity removes -0.0, 0.0 changes to files.
        """
        if x == CuratorConstants.VALUE_INFEASIBLE:
            return x
        else:
            x = round(x, self.num_decimals)
            if abs(x) < 1e-10:
                x = abs(x)
            return x

    def write_results(self, path_out: Path):
        """Write results to path."""
        if not path_out.exists():
            logger.warning(f"Creating results path: {path_out}")
            path_out.mkdir(parents=True)

        # write metadata file
        with open(path_out / CuratorConstants.METADATA_FILENAME, "w") as f_json:
            json.dump(self.metadata, fp=f_json, indent=2)

        # write reference files
        for filename, df in dict(
            zip(
                [
                    CuratorConstants.OBJECTIVE_FILENAME,
                    CuratorConstants.FVA_FILENAME,
                    CuratorConstants.GENE_DELETION_FILENAME,
                    CuratorConstants.REACTION_DELETION_FILENAME,
                ],
                [self.objective, self.fva, self.gene_deletion, self.reaction_deletion],
            )
        ).items():
            logger.debug(f"-> {path_out / filename}")
            df.to_csv(path_out / filename, sep="\t", index=False)
            # df.to_json(path_out / filename, sep="\t", index=False)

    @classmethod
    def read_results(cls, path_in: Path):
        """Read fbc curation files from given directory."""
        path_metadata = path_in / CuratorConstants.METADATA_FILENAME
        path_objective = path_in / CuratorConstants.OBJECTIVE_FILENAME
        path_fva = path_in / CuratorConstants.FVA_FILENAME
        path_gene_deletion = path_in / CuratorConstants.GENE_DELETION_FILENAME
        path_reaction_deletion = path_in / CuratorConstants.REACTION_DELETION_FILENAME
        df_dict = dict()

        for k, path in enumerate(
            [path_objective, path_fva, path_gene_deletion, path_reaction_deletion]
        ):
            if not path_objective.exists():
                logger.error(f"Required file for fbc curation does not exist: '{path}'")
            else:
                df_dict[CuratorConstants.KEYS[k]] = pd.read_csv(path, sep="\t")

        with open(path_metadata, "r") as f_json:
            df_dict[CuratorConstants.METADATA_KEY] = json.load(fp=f_json)
        objective_id = df_dict["objective"].objective.values[0]

        return FROGResults(objective_id=objective_id, **df_dict)

    @staticmethod
    def compare(results: Dict[str, "FROGResults"]) -> bool:
        """Compare results against each other.

        Returns True of all results are identical.
        """
        curator_keys = list(results.keys())
        curator_results = list(results.values())
        keys = list(results.keys())
        num_res = len(curator_results)
        # only comparing comparison between two data frames

        console.rule("Comparison of results", style="white", align="left")
        all_equal = True

        for key in CuratorConstants.KEYS:
            mat_equal = np.ndarray(shape=(num_res, num_res))
            for p, res1 in enumerate(curator_results):
                for q, res2 in enumerate(curator_results):
                    df1 = getattr(res1, key)
                    df2 = getattr(res2, key)
                    if df1.equals(df2):
                        equal = 1
                    else:
                        equal = 0
                    mat_equal[p, q] = equal

                    if equal == 0:
                        console.print(
                            f"difference: '{curator_keys[p]}' vs '{curator_keys[q]}'"
                        )
                        FROGResults.analyse_df_difference(df1, df2)

            df_equal = pd.DataFrame(
                mat_equal, columns=list(keys), index=list(keys), dtype=int
            )
            console.print(f"--- {key} ---")
            console.print(df_equal)
            all_equal = (
                all_equal and np.sum(np.sum(df_equal.values)) == num_res * num_res
            )

        console.rule(style="white")
        console.print(f"Equal: {all_equal}")
        console.rule(style="white")
        return bool(all_equal)

    @staticmethod
    def analyse_df_difference(df1: pd.DataFrame, df2: pd.DataFrame):
        """Analyse DataFrame difference."""
        df_diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
        console.print(df_diff)

    def validate(self) -> bool:
        """Validate results."""
        # Load the data and validate
        # FIXME: implement
        pass
