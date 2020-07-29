from pathlib import Path
import pandas as pd
import libsbml
from fbc_curation import EXAMPLE_PATH
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
from fbc_curation.constants import CuratorConstants

model_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"
curator = CuratorCobrapy(model_path=model_path)
results = curator.run()
doc = libsbml.readSBMLFromFile(str(model_path))  # type: libsbml.SBMLDocument
model = doc.getModel()  # type: libsbml.Model


def test_objective_df():
    df = results.objective
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == len(CuratorConstants.OBJECTIVE_FIELDS)
    for field in CuratorConstants.OBJECTIVE_FIELDS:
        assert field in df.columns
    for k, field in enumerate(CuratorConstants.OBJECTIVE_FIELDS):
        assert df.columns[k] == field

    obj_value = df['value'].values[0]
    assert obj_value > 0

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_fva_df():
    df = results.fva
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == len(CuratorConstants.FVA_FIELDS)
    for field in CuratorConstants.FVA_FIELDS:
        assert field in df.columns
    for k, field in enumerate(CuratorConstants.FVA_FIELDS):
        assert df.columns[k] == field

    assert len(df) == model.getNumReactions()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_gene_deletion():
    df = results.gene_deletion
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == len(CuratorConstants.GENE_DELETION_FIELDS)
    for field in CuratorConstants.GENE_DELETION_FIELDS:
        assert field in df.columns
    for k, field in enumerate(CuratorConstants.GENE_DELETION_FIELDS):
        assert df.columns[k] == field

    fbc_model = model.getPlugin("fbc")  # type: libsbml.FbcModelPlugin
    assert len(df) == fbc_model.getNumGeneProducts()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_reaction_deletion(tmp_path):
    df = results.reaction_deletion
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == len(CuratorConstants.REACTION_DELETION_FIELDS)
    for field in CuratorConstants.REACTION_DELETION_FIELDS:
        assert field in df.columns
    for k, field in enumerate(CuratorConstants.REACTION_DELETION_FIELDS):
        assert df.columns[k] == field

    assert len(df) == model.getNumReactions()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes
