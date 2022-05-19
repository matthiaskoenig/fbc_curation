"""Comparison of FROG results."""
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from pymetadata import log
from pymetadata.console import console
from pymetadata.omex import EntryFormat, Omex

from fbc_curation import EXAMPLE_DIR
from fbc_curation.frog import CuratorConstants, FrogReport


logger = log.get_logger(__name__)


class FrogComparison:
    """FrogComparison.

    Class for comparing FROG reports. Allows to check if multiple FROGs
    give the same results.
    """

    absolute_tolerance: float = 1e-3
    relative_tolerance: float = 1e-3

    @staticmethod
    def read_reports_from_omex(omex_path: Path) -> Dict[str, Dict[str, FrogReport]]:
        """Read all reports from JSON and TSVs.

        Returns dictionary of {model_location: ...}

        """
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
                logger.error(
                    f"duplicate FROG report: '{frog_id}' for '{model_location}'"
                )
            d[frog_id] = report
            model_reports[model_location] = d

        info = {loc: list(item.keys()) for loc, item in model_reports.items()}
        logger.info(f"Reports in omex:\n{info}")

        return model_reports

    # TODO: implement comparison result and return results

    @staticmethod
    def compare_reports(reports: Dict[str, FrogReport]) -> bool:
        """Compare results against each other.

        Compare all matrices pairwise, i.e., comparison matrix for
        - objective
        - FVA
        - gene deletions
        - reaction deletions
        """
        console.rule("Comparison of FROGReports", style="white")

        num_reports = len(reports)
        all_equal: bool = True
        # only comparing comparison between two data frames

        data: Dict[str, Dict[str, pd.DataFrame]] = {}

        # DataFrames for report
        report_keys = list(reports.keys())
        for report_key, report in reports.items():
            # all DataFrames for single report
            frog_dfs: Dict[str, pd.DataFrame] = report.to_dfs()
            data[report_key] = frog_dfs

        # Perform comparisons between all reports
        for key in [
            CuratorConstants.OBJECTIVE_KEY,
            CuratorConstants.FVA_KEY,
            CuratorConstants.REACTIONDELETIONS_KEY,
            CuratorConstants.GENEDELETIONS_KEY,
        ]:
            mat_equal = np.zeros(shape=(num_reports, num_reports))

            # do all pairwise comparisons
            dfs: List[pd.DataFrame] = [
                data[report_key][key] for report_key in reports.keys()
            ]
            for p, df1 in enumerate(dfs):
                for q, df2 in enumerate(dfs):

                    fields: List[str]
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
                        if field in df1.columns and field in df2.columns:
                            equal_field = np.allclose(
                                df1[field].values,
                                df2[field].values,
                                atol=FrogComparison.absolute_tolerance,
                                rtol=FrogComparison.relative_tolerance,
                                equal_nan=True,
                            )
                            equal = equal and equal_field

                    mat_equal[p, q] = int(equal)

                    if not equal:
                        logger.warning(
                            f"difference: '{report_keys[p]}' vs '{report_keys[q]}'"
                        )
                        equal_vec = np.isclose(
                            df1[field].values,
                            df2[field].values,
                            atol=FrogComparison.absolute_tolerance,
                            rtol=FrogComparison.relative_tolerance,
                            equal_nan=True,
                        )
                        df_diff = pd.concat([df1[~equal_vec], df2[~equal_vec]])
                        if "reaction" in df_diff.columns:
                            df_diff.sort_values(by=["reaction"], inplace=True)
                        elif "gene" in df_diff.columns:
                            df_diff.sort_values(by=["gene"], inplace=True)
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
        return bool(all_equal)


if __name__ == "__main__":
    # Read results and compare
    omex_path = EXAMPLE_DIR / "frogs" / "e_coli_core_FROG.omex"
    model_reports = FrogComparison.read_reports_from_omex(omex_path=omex_path)
    for model_location, reports in model_reports.items():
        print(model_location)
        FrogComparison.compare_reports(reports)
