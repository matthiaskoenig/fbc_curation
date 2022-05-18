"""Test the fbc_curation on the examples."""
from pathlib import Path

import pytest

from fbc_curation import examples
from fbc_curation.frog import CuratorConstants
from pymetadata.omex import Omex


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


def test_e_coli_core(tmp_path: Path):
    """Test fbc_curation."""
    omex_path = examples.example_ecoli_core()
    omex = Omex.from_omex(omex_path)
    omex.to_directory(tmp_path / "frog")

    _check_tmp_path(tmp_path / "frog")
