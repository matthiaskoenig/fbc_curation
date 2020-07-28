from pathlib import Path
from fbc_curation import examples
from fbc_curation.constants import CuratorConstants


def _check_tmp_path(path):
    for curator_key in ["cobrapy", "cameo"]:
        assert Path.exists(path / curator_key / CuratorConstants.FILENAME_OBJECTIVE_FILE)
        assert Path.exists(path / curator_key / CuratorConstants.FILENAME_FVA_FILE)
        assert Path.exists(path / curator_key / CuratorConstants.FILENAME_REACTION_DELETION_FILE)
        assert Path.exists(path / curator_key / CuratorConstants.FILENAME_GENE_DELETION_FILE)


def test_e_coli_core(tmp_path):
    examples.example_ecoli_core(tmp_path)
    _check_tmp_path(tmp_path)


def test_iJR904(tmp_path):
    examples.example_iJR904(tmp_path)
    _check_tmp_path(tmp_path)


def test_iAB_AMO1410_SARS(tmp_path):
    examples.example_iAB_AMO1410_SARS(tmp_path)
    _check_tmp_path(tmp_path)

