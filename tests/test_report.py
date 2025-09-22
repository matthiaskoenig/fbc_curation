"""Testing result."""
from pathlib import Path
from typing import Dict

import libsbml
import pandas as pd

from fbc_curation import EXAMPLE_DIR
from fbc_curation.compare import FrogComparison
from fbc_curation.curator.cobrapy_curator import Creator, CuratorCobrapy
from fbc_curation.frog import CuratorConstants, FrogReport


model_path: Path = EXAMPLE_DIR / "models" / "e_coli_core.xml"
frog_id: str = "1234"
curators = [
    Creator(
        familyName="König",
        givenName="Matthias",
    )
]
curator = CuratorCobrapy(model_path=model_path, frog_id=frog_id, curators=curators)
report: FrogReport = curator.run()
doc: libsbml.SBMLDocument = libsbml.readSBMLFromFile(str(model_path))
model: libsbml.Model = doc.getModel()


def test_objective_df() -> None:
    """Check objective."""
    dfs: Dict[str, pd.DataFrame] = report.to_dfs()
    df = dfs[CuratorConstants.OBJECTIVE_KEY]

    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    obj_value = df["value"].values[0]
    assert obj_value > 0

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_fva_df() -> None:
    """Check FVA DataFrame."""
    dfs: Dict[str, pd.DataFrame] = report.to_dfs()
    df = dfs[CuratorConstants.FVA_KEY]

    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    assert len(df) == model.getNumReactions()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_gene_deletion_df() -> None:
    """Check gene deletion."""
    dfs: Dict[str, pd.DataFrame] = report.to_dfs()
    df = dfs[CuratorConstants.GENE_DELETION_KEY]
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    fbc_model: libsbml.FbcModelPlugin = model.getPlugin("fbc")
    assert len(df) == fbc_model.getNumGeneProducts()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_reaction_deletion_df(tmp_path: Path) -> None:
    """Check reaction deletion."""
    dfs: Dict[str, pd.DataFrame] = report.to_dfs()
    df: pd.DataFrame = dfs[CuratorConstants.REACTION_DELETION_KEY]
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    assert len(df) == model.getNumReactions()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_report_write_read_tsv_equal(tmp_path: Path) -> None:
    """Test equality of report after writing/reading TSV."""
    report.to_tsv(tmp_path)
    report2 = FrogReport.from_tsv(tmp_path)

    assert FrogComparison.compare_reports({"report": report, "report2": report2})


def test_report_write_read_json_equal(tmp_path: Path) -> None:
    """Test equality of report after writing/reading JSON."""
    report.to_json(path=tmp_path / "frog.json")
    report2 = FrogReport.from_json(path=tmp_path / "frog.json")

    assert FrogComparison.compare_reports({"report": report, "report2": report2})
