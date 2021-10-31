"""Test the fbc_curation on the examples."""
from pathlib import Path

import pytest

from fbc_curation import examples
from fbc_curation.frog import CuratorConstants


def _check_tmp_path(path):
    for curator_key in ["cobrapy", "cameo"]:
        assert Path.exists(path / curator_key / CuratorConstants.OBJECTIVE_FILENAME)
        assert Path.exists(path / curator_key / CuratorConstants.FVA_FILENAME)
        assert Path.exists(
            path / curator_key / CuratorConstants.REACTIONDELETIONS_FILENAME
        )
        assert Path.exists(path / curator_key / CuratorConstants.GENEDELETIONS_FILENAME)


def _check_example_results(res):
    assert res["valid"] == [True, True]
    assert res["equal"]


def test_e_coli_core(tmp_path):
    """Test fbc_curation."""
    res = examples.example_ecoli_core(tmp_path)
    _check_tmp_path(tmp_path)
    _check_example_results(res)


@pytest.mark.skip(reason="Reduce runtime")
def test_iJR904(tmp_path):
    """Test fbc_curation."""
    res = examples.example_iJR904(tmp_path)
    _check_tmp_path(tmp_path)
    _check_example_results(res)


@pytest.mark.skip(reason="reduce runtime")
def test_iAB_AMO1410_SARS(tmp_path):
    """Test fbc_curation."""
    res = examples.example_iAB_AMO1410_SARS(tmp_path)
    _check_tmp_path(tmp_path)
    _check_example_results(res)
