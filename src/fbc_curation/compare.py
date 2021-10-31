"""Comparison of FROG results."""
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


class Comparison:
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
                        Comparison.analyse_df_difference(df1, df2)

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
        raise NotImplementedError

    # def _round_and_sort(self):
    #     """Round and sort."""
    #     # FIXME: processing must be done on creating the files ?!
    #     # round and sort objective value
    #     for key in ["value"]:
    #         self.objective[key] = self.objective[key].apply(self._round)
    #     self.objective.sort_values(by=["objective"], inplace=True)
    #
    #     # round and sort fva
    #     for key in ["flux", "minimum", "maximum"]:
    #         self.fva[key] = self.fva[key].apply(self._round)
    #     self.fva.sort_values(by=["reaction"], inplace=True)
    #     self.fva.index = range(len(self.fva))
    #
    #     # round and sort gene_deletion
    #     for key in ["value"]:
    #         self.gene_deletion[key] = self.gene_deletion[key].apply(self._round)
    #     self.gene_deletion.sort_values(by=["gene"], inplace=True)
    #     self.gene_deletion.index = range(len(self.gene_deletion))
    #
    #     # round and sort reaction deletion
    #     for key in ["value"]:
    #         self.reaction_deletion[key] = self.reaction_deletion[key].apply(self._round)
    #     self.reaction_deletion.sort_values(by=["reaction"], inplace=True)
    #     self.reaction_deletion.index = range(len(self.reaction_deletion))
    #
    #     # validate
    #     self.validate()
    #
    # def _round(self, x):
    #     """Round the float and sets small values positive.
    #
    #     Ensuring positivity removes -0.0, 0.0 changes to files.
    #     """
    #     if x == CuratorConstants.VALUE_INFEASIBLE:
    #         return x
    #     else:
    #         x = round(x, self.num_decimals)
    #         if abs(x) < 1e-10:
    #             x = abs(x)
    #         return x
