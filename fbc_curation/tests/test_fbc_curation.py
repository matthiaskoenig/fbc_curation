from pathlib import Path
import pandas as pd
from fbc_curation import FBCFileCreator, EXAMPLE_PATH

model_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"


def test_objective_value(tmp_path):
    creator = FBCFileCreator(
        model_path=model_path,
        results_path=tmp_path
    )
    df = creator.create_objective_file("test.tsv")
    assert Path.exists(tmp_path / "test.tsv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == 4

    assert "model" in df.columns
    assert "objective" in df.columns
    assert "status" in df.columns
    assert "value" in df.columns
    assert df.columns[0] == "model"
    assert df.columns[1] == "objective"
    assert df.columns[2] == "status"
    assert df.columns[3] == "value"

    obj_value = df['value'].values[0]
    assert obj_value > 0

    # without filename the default filenames are used
    creator.create_objective_file()
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_OBJECTIVE_FILE)


def test_fva(tmp_path):
    creator = FBCFileCreator(
        model_path=model_path,
        results_path=tmp_path
    )
    df = creator.create_fva_file(filename="test.tsv")
    assert Path.exists(tmp_path / "test.tsv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == 6
    assert "model" in df.columns
    assert "objective" in df.columns
    assert "reaction" in df.columns
    assert "status" in df.columns
    assert "minimum" in df.columns
    assert "maximum" in df.columns
    assert df.columns[0] == "model"
    assert df.columns[1] == "objective"
    assert df.columns[2] == "reaction"
    assert df.columns[3] == "status"
    assert df.columns[4] == "minimum"
    assert df.columns[5] == "maximum"

    model = creator.read_cobra_model()
    assert len(df) == len(model.reactions)

    df = creator.create_fva_file()
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_FVA_FILE)


def test_gene_deletion(tmp_path):
    creator = FBCFileCreator(
        model_path=model_path,
        results_path=tmp_path
    )
    df = creator.create_gene_deletion_file("test.tsv")
    assert Path.exists(tmp_path / "test.tsv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == 5
    assert "model" in df.columns
    assert "objective" in df.columns
    assert "gene" in df.columns
    assert "status" in df.columns
    assert "value" in df.columns
    assert df.columns[0] == "model"
    assert df.columns[1] == "objective"
    assert df.columns[2] == "gene"
    assert df.columns[3] == "status"
    assert df.columns[4] == "value"


    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes

    model = creator.read_cobra_model()
    assert len(df) == len(model.genes)

    df = creator.create_gene_deletion_file()
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_GENE_DELETION_FILE)


def test_reaction_deletion(tmp_path):
    creator = FBCFileCreator(
        model_path=model_path,
        results_path=tmp_path
    )
    df = creator.create_reaction_deletion_file("test.tsv")
    assert Path.exists(tmp_path / "test.tsv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == 5
    assert "model" in df.columns
    assert "objective" in df.columns
    assert "reaction" in df.columns
    assert "status" in df.columns
    assert "value" in df.columns
    assert df.columns[0] == "model"
    assert df.columns[1] == "objective"
    assert df.columns[2] == "reaction"
    assert df.columns[3] == "status"
    assert df.columns[4] == "value"

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes

    model = creator.read_cobra_model()
    assert len(df) == len(model.reactions)

    df = creator.create_reaction_deletion_file()
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_REACTION_DELETION_FILE)
