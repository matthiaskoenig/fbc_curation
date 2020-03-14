from pathlib import Path
from fbc_curation import examples


def test_e_coli_core(tmp_path):
    examples.example_ecoli_core(tmp_path)
    assert Path.exists(tmp_path / "e_coli_core_01_objective.tsv")
    assert Path.exists(tmp_path / "e_coli_core_02_fva.tsv")
    assert Path.exists(tmp_path / "e_coli_core_03_gene_deletion.tsv")
    assert Path.exists(tmp_path / "e_coli_core_04_reaction_deletion.tsv")


def test_iJR904(tmp_path):
    examples.example_iJR904(tmp_path)
    assert Path.exists(tmp_path / "iJR904_01_objective.tsv")
    assert Path.exists(tmp_path / "iJR904_02_fva.tsv")
    assert Path.exists(tmp_path / "iJR904_03_gene_deletion.tsv")
    assert Path.exists(tmp_path / "iJR904_04_reaction_deletion.tsv")


def test_MODEL1709260000(tmp_path):
    examples.example_MODEL1709260000(tmp_path)
    assert Path.exists(tmp_path / "MODEL1709260000_01_objective.tsv")
    assert Path.exists(tmp_path / "MODEL1709260000_02_fva.tsv")
    assert Path.exists(tmp_path / "MODEL1709260000_03_gene_deletion.tsv")
    assert Path.exists(tmp_path / "MODEL1709260000_04_reaction_deletion.tsv")
