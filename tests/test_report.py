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


def _check_objective(df):
    """Check objective DataFrame."""
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    obj_value = df["value"].values[0]
    assert obj_value > 0

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_objective() -> None:
    """Check objective."""
    dfs: Dict[str, pd.DataFrame] = report.to_dfs()
    _check_objective(dfs[CuratorConstants.OBJECTIVE_KEY])


def _check_fva(df):
    """Check FVA."""
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    assert len(df) == model.getNumReactions()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_fva():
    """Check FVA DataFrame."""
    dfs: Dict[str, pd.DataFrame] = report.to_dfs()
    _check_fva(dfs[CuratorConstants.FVA_KEY])


def _check_gene_deletion(df):
    """Check gene deletion."""
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    fbc_model: libsbml.FbcModelPlugin = model.getPlugin("fbc")
    assert len(df) == fbc_model.getNumGeneProducts()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_gene_deletion() -> None:
    """Check gene deletion."""
    dfs: Dict[str, pd.DataFrame] = report.to_dfs()
    _check_gene_deletion(dfs[CuratorConstants.GENEDELETIONS_KEY])


def _check_reaction_deletion(df: pd.DataFrame) -> None:
    """Check reaction deletion."""
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    assert len(df) == model.getNumReactions()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_reaction_deletion(tmp_path) -> None:
    """Check reaction deletion."""
    dfs: Dict[str, pd.DataFrame] = report.to_dfs()
    _check_reaction_deletion(dfs[CuratorConstants.REACTIONDELETIONS_KEY])


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
