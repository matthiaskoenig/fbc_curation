from pathlib import Path
from fbc_curation import examples
from fbc_curation.constants import CuratorConstants


def _check_tmp_path(path):
    for curator_key in ["cobrapy", "cameo"]:
        assert Path.exists(path / curator_key / CuratorConstants.OBJECTIVE_FILENAME)
        assert Path.exists(path / curator_key / CuratorConstants.FVA_FILENAME)
        assert Path.exists(path / curator_key / CuratorConstants.REACTION_DELETION_FILENAME)
        assert Path.exists(path / curator_key / CuratorConstants.GENE_DELETION_FILENAME)


def test_e_coli_core(tmp_path):
    examples.example_ecoli_core(tmp_path)
    _check_tmp_path(tmp_path)


def test_iJR904(tmp_path):
    examples.example_iJR904(tmp_path)
    _check_tmp_path(tmp_path)


def test_iAB_AMO1410_SARS(tmp_path):
    examples.example_iAB_AMO1410_SARS(tmp_path)
    _check_tmp_path(tmp_path)
