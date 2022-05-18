"""Test the fbc_curation on the examples."""
from pathlib import Path

from pymetadata.omex import Omex

from fbc_curation import examples
from fbc_curation.frog import CuratorConstants


def _check_tmp_path(path):
    for curator_key in ["cobrapy", "cameo"]:
        base_path = path / "FROG" / curator_key
        assert Path.exists(base_path / CuratorConstants.OBJECTIVE_FILENAME)
        assert Path.exists(base_path / CuratorConstants.FVA_FILENAME)
        assert Path.exists(base_path / CuratorConstants.REACTIONDELETIONS_FILENAME)
        assert Path.exists(base_path / CuratorConstants.GENEDELETIONS_FILENAME)


def _check_example_results(res):
    assert res["valid"] == [True, True]
    assert res["equal"]


def test_e_coli_core(tmp_path: Path):
    """Test fbc_curation."""
    omex_path = examples.run_example("e_coli_core.xml")
    omex = Omex.from_omex(omex_path)
    print(omex)
    omex.to_directory(tmp_path / "frog")

    _check_tmp_path(tmp_path / "frog")
