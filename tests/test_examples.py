"""Test the fbc_curation on the examples."""
from pathlib import Path

import pytest
from pymetadata.omex import Omex

from fbc_curation import examples
from fbc_curation.frog import CuratorConstants


@pytest.mark.parametrize("curator_key", ["cobrapy", "cameo"])
def test_e_coli_core(tmp_path: Path, curator_key: str) -> None:
    """Test fbc_curation."""
    omex_path = examples.run_example("e_coli_core.xml")
    omex = Omex.from_omex(omex_path)
    omex.to_directory(tmp_path)

    base_path = tmp_path / "FROG" / curator_key
    assert Path.exists(base_path / CuratorConstants.OBJECTIVE_FILENAME)
    assert Path.exists(base_path / CuratorConstants.FVA_FILENAME)
    assert Path.exists(base_path / CuratorConstants.REACTIONDELETIONS_FILENAME)
    assert Path.exists(base_path / CuratorConstants.GENEDELETIONS_FILENAME)
