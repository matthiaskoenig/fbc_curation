from pathlib import Path
import pytest
import pandas as pd
import fbc_curation
import examples
from fbc_curation import read_sbml_model

base_dir = Path(__file__).parent
model_path = base_dir / "models" / "e_coli_core.xml"


def test_objective_value(tmp_path):
    model = read_sbml_model(str(model_path))
    results_path = tmp_path / "test.tsv"
    obj_value = fbc_curation.create_objective_file(model, results_path)
    assert isinstance(obj_value, float)
    assert obj_value > 0
    assert Path.exists(results_path)


def test_fva(tmp_path):
    model = read_sbml_model(str(model_path))
    results_path = tmp_path / "test.tsv"
    df = fbc_curation.create_fva_file(model, results_path)
    assert not df.empty
    assert Path.exists(results_path)

    assert len(df) == len(model.reactions)
    assert "reaction" in df.columns
    assert "minimum" in df.columns
    assert "maximum" in df.columns


def test_gene_deletion(tmp_path):
    model = read_sbml_model(str(model_path))
    results_path = tmp_path / "test.tsv"
    df = fbc_curation.create_gene_deletion_file(model, results_path)
    assert not df.empty
    assert Path.exists(results_path)

    assert len(df) == len(model.genes)
    assert "gene" in df.columns
    assert "value" in df.columns
    assert "status" in df.columns


def test_reaction_deletion(tmp_path):
    model = read_sbml_model(str(model_path))
    results_path = tmp_path / "test.tsv"
    df = fbc_curation.create_reaction_deletion_file(model, results_path)
    assert not df.empty
    assert Path.exists(results_path)

    assert len(df) == len(model.reactions)
    assert "reaction" in df.columns
    assert "value" in df.columns
    assert "status" in df.columns


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
