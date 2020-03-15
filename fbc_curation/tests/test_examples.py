from pathlib import Path
from fbc_curation import examples
from fbc_curation import FBCFileCreator


def test_e_coli_core(tmp_path):
    examples.example_ecoli_core(tmp_path)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_OBJECTIVE_FILE)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_FVA_FILE)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_REACTION_DELETION_FILE)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_GENE_DELETION_FILE)


def test_iJR904(tmp_path):
    examples.example_iJR904(tmp_path)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_OBJECTIVE_FILE)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_FVA_FILE)
    assert Path.exists(
        tmp_path / FBCFileCreator.FILENAME_REACTION_DELETION_FILE)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_GENE_DELETION_FILE)


def test_MODEL1709260000(tmp_path):
    examples.example_MODEL1709260000(tmp_path)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_OBJECTIVE_FILE)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_FVA_FILE)
    assert Path.exists(
        tmp_path / FBCFileCreator.FILENAME_REACTION_DELETION_FILE)
    assert Path.exists(tmp_path / FBCFileCreator.FILENAME_GENE_DELETION_FILE)
