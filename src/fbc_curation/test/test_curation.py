"""Test fbc_curation command line script."""

import sys

import pytest

from fbc_curation import EXAMPLE_PATH, runfrog


@pytest.mark.parametrize("filename", ["e_coli_core.xml", "iJR904.xml.gz"])
def test_runfrog1(monkeypatch, tmp_path, filename):
    """First example via command line tool.

    runfrog --model resources/examples/models/e_coli_core.xml
    --path resources/examples/results/e_coli_core
    """
    with monkeypatch.context() as m:
        args = [
            "runfrog",
            "--model",
            f"{EXAMPLE_PATH / 'models' / filename}",
            "--path",
            str(tmp_path),
        ]
        m.setattr(sys, "argv", args)
        runfrog.main()
        # FIXME: check results files
        for out_fname in ["frogreport.json"]:
            assert (tmp_path / "cobrapy" / out_fname).exists()
            assert (tmp_path / "cameo" / out_fname).exists()


def test_runfrog2(monkeypatch, tmp_path):
    """Second example via command line tool.

    runfrog --model resources/examples/models/e_coli_core.xml
    --path resources/examples/results/e_coli_core
    --reference resources/examples/results/e_coli_core/cobrapy
    """
    with monkeypatch.context() as m:
        args = [
            "runfrog",
            "--model",
            f"{EXAMPLE_PATH / 'models' / 'e_coli_core.xml'}",
            "--path",
            str(tmp_path),
            "--reference",
            f"{EXAMPLE_PATH / 'results' / 'e_coli_core' / 'cobrapy'}",
        ]
        m.setattr(sys, "argv", args)
        runfrog.main()
        for out_fname in ["frogreport.json"]:
            assert (tmp_path / "cobrapy" / out_fname).exists()
            assert (tmp_path / "cameo" / out_fname).exists()
