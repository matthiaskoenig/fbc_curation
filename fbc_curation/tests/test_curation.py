import sys
from fbc_curation import curation, EXAMPLE_PATH
from fbc_curation.constants import CuratorConstants
import pytest


@pytest.mark.parametrize('filename', ['e_coli_core.xml', 'iJR904.xml.gz'])
def test_curation(monkeypatch, tmp_path, filename):
    """
    curation --model ../examples/models/e_coli_core.xml --path ../examples/results/e_coli_core
    """
    with monkeypatch.context() as m:
        args = [
            'curation',
            '--model', f"{EXAMPLE_PATH / 'models' / filename}",
            '--path', str(tmp_path)
        ]
        m.setattr(sys, 'argv', args)
        curation.main()
        for out_fname in CuratorConstants.FILENAMES:
            assert (tmp_path / 'cobrapy' / out_fname).exists()
            assert (tmp_path / 'cameo' / out_fname).exists()
