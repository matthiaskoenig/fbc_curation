"""Test fbc_curation command line script."""

import sys

import pytest

from fbc_curation import EXAMPLE_PATH, curation
from fbc_curation.constants import CuratorConstants


@pytest.mark.parametrize("filename", ["e_coli_core.xml", "iJR904.xml.gz"])
def test_curation1(monkeypatch, tmp_path, filename):
    """First example via command line tool.

    curation --model ../examples/models/e_coli_core.xml
    --path ../examples/results/e_coli_core
    """
    with monkeypatch.context() as m:
        args = [
            "curation",
            "--model",
            f"{EXAMPLE_PATH / 'models' / filename}",
            "--path",
            str(tmp_path),
        ]
        m.setattr(sys, "argv", args)
        curation.main()
        for out_fname in CuratorConstants.FILENAMES:
            assert (tmp_path / "cobrapy" / out_fname).exists()
            assert (tmp_path / "cameo" / out_fname).exists()


def test_curation2(monkeypatch, tmp_path):
    """Second example via command line tool.

    curation --model examples/models/e_coli_core.xml
    --path examples/results/e_coli_core
    --reference ../examples/results/e_coli_core/cobrapy
    """
    with monkeypatch.context() as m:
        args = [
            "curation",
            "--model",
            f"{EXAMPLE_PATH / 'models' / 'e_coli_core.xml'}",
            "--path",
            str(tmp_path),
            "--reference",
            f"{EXAMPLE_PATH / 'results' / 'e_coli_core' / 'cobrapy'}",
        ]
        m.setattr(sys, "argv", args)
        curation.main()
        for out_fname in CuratorConstants.FILENAMES:
            assert (tmp_path / "cobrapy" / out_fname).exists()
            assert (tmp_path / "cameo" / out_fname).exists()
