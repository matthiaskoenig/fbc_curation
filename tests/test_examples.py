"""Test the fbc_curation on the examples."""
from pathlib import Path

import pytest
from pymetadata.omex import Omex

from fbc_curation import FROG_PATH_PREFIX, examples
from fbc_curation.frog import CuratorConstants


@pytest.mark.parametrize("curator_key", ["cobrapy", "cameo"])
def test_e_coli_core(tmp_path: Path, curator_key: str) -> None:
    """Test fbc_curation."""
    omex_path = examples.run_example("e_coli_core.xml")
    omex = Omex.from_omex(omex_path)
    omex.to_directory(tmp_path)

    for curator_key in ["cobrapy", "cameo"]:
        base_path = tmp_path / FROG_PATH_PREFIX / curator_key
        assert Path.exists(base_path / CuratorConstants.OBJECTIVE_FILENAME)
        assert Path.exists(base_path / CuratorConstants.FVA_FILENAME)
        assert Path.exists(base_path / CuratorConstants.REACTION_DELETION_FILENAME)
        assert Path.exists(base_path / CuratorConstants.GENE_DELETION_FILENAME)
