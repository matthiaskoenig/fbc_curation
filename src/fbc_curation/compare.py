"""Comparison of FROG results."""
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from pydantic import BaseModel
from pymetadata import log
from pymetadata.console import console
from pymetadata.omex import Omex, EntryFormat

from fbc_curation.frog import CuratorConstants, FrogReport


logger = log.get_logger(__name__)


# Reading reference solution
# res_dict: Dict[str, FrogReport] = {}
# if reference_path:
#     reference_results = FrogReport.read_results(reference_path)
#     res_dict["reference"] = reference_results
#
# for k, curator_class in enumerate(curator_classes):
#     key = curator_keys[k]
#     curator = curator_class(model_path=model_path, objective_id=objective_id)
#     results = curator.run()  # type: FROGResults
#     results.write_results(output_path / key)
#     res_dict[key] = FrogReport.read_results(output_path / key)
#
# # perform comparison
# if len(res_dict) > 1:
#     FrogReport.compare(res_dict)


class ComparisonResult:
    keys: List[str]
    fva: pd.DataFrame


class Comparison:

    absolute_tolerance = 1e-6
    relative_tolerance = 1e-6

    @staticmethod
    def read_reports_from_omex(omex_path: Path):
        """Read all reports from JSON and TSVs."""
        reports: List[FrogReport] = []
        omex = Omex.from_omex(omex_path)
        for entry in omex.manifest.entries:
            if entry.format == EntryFormat.FROG_JSON_V1:
                report = FrogReport.from_json(path=omex.get_path(entry.location))
                reports.append(report)
            elif entry.format == EntryFormat.FROG_METADATA_V1:
                path = omex.get_path(entry.location).parent
                report = FrogReport.from_tsv(path)
                reports.append(report)

        # get model reports per model
        model_reports: Dict[str, Dict[str, FrogReport]] = {}
        for report in reports:
            model_location = report.metadata.model_location
            d = model_reports.get(model_location, {})
            frog_id = report.metadata.frog_id
            if frog_id in d:
                logger.error(f"duplicate FROG report: '{frog_id}' for '{model_location}'")
            d[frog_id] = report
            model_reports[model_location] = d

        for location, reports_dict in model_reports.items():
            logger.info(f"{location}: {reports_dict.keys()}")

    @staticmethod
    def compare(reports: Dict[str, FrogReport]) -> None:
        """Compare results against each other.

        Compares all matrices pairwise, i.e., comparison matrix for
        - objective
        - FVA
        - gene deletions
        - reaction deletions
        """

        num_reports = len(reports)
        # only comparing comparison between two data frames

        console.rule("Comparison of reports", style="white")

        data: Dict[str, Dict[str, pd.DataFrame]] = {}

        # DataFrames for report
        report_keys = list(reports.keys())
        for report_key, report in reports.items():
            dfs = report.to_dfs()
            data[report_key] = dfs

        # Perform all comparisons
        for key in [
            CuratorConstants.OBJECTIVE_KEY,
            CuratorConstants.FVA_KEY,
            CuratorConstants.REACTIONDELETIONS_KEY,
            CuratorConstants.GENEDELETIONS_KEY,
        ]:
            mat_equal = np.zeros(shape=(num_reports, num_reports))

            # do all pairwise comparisons
            dfs = [data[report_key][key] for report_key in reports.keys()]
            for p, df1 in enumerate(dfs):
                for q, df2 in enumerate(dfs):

                    equal = True
                    if key in [
                        CuratorConstants.OBJECTIVE_KEY,
                        CuratorConstants.REACTIONDELETIONS_KEY,
                        CuratorConstants.GENEDELETIONS_KEY,
                    ]:
                        fields = ["value"]
                    elif key == CuratorConstants.FVA_KEY:
                        fields = ["flux", "minimum", "maximum"]

                    for field in fields:
                        equal_field = np.allclose(
                            df1[field].values,
                            df2[field].values,
                            atol=Comparison.absolute_tolerance,
                            rtol=Comparison.relative_tolerance,
                        )
                        equal = equal and equal_field

                    mat_equal[p, q] = int(equal)

                    if not equal:
                        console.warning(
                            f"difference: '{report_keys[p]}' vs '{report_keys[q]}'"
                        )
                        df_diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
                        console.print(df_diff)

            df_equal = pd.DataFrame(
                mat_equal, columns=list(report_keys), index=list(report_keys), dtype=int
            )
            console.print(f"--- {key} ---")
            console.print(df_equal)
            all_equal = (
                all_equal
                and np.sum(np.sum(df_equal.values)) == num_reports * num_reports
            )

        console.rule(style="white")
        console.print(f"Equal: {all_equal}")
        console.rule(style="white")
        # return bool(all_equal)


if __name__ == "__main__":
    # Read results and compare
    pass
