"""
Module for creating FBC curation files via cobrapy.

Uses GLPK as default solver.
"""
import pandas as pd
import cobra
from cobra.io import read_sbml_model
from pathlib import Path

from cobra.flux_analysis import flux_variability_analysis
from cobra.flux_analysis import single_gene_deletion, single_reaction_deletion


def create_fbc_files(model_path: Path, results_dir) -> pd.DataFrame:
    """ Creates all FBC curation files

    Model is reloaded for different files to make sure
    simulations are run from the initial model state.

    :param model_path:
    :param results_dir:
    :return:
    """
    # objective value
    mpath = str(model_path)
    model = read_sbml_model(mpath)
    mid = model.id
    create_objective_file(model, results_dir / f"{mid}_01_objective.tsv")

    # flux variability
    mpath = str(model_path)
    model = read_sbml_model(mpath)
    mid = model.id
    create_fva_file(model, results_dir / f"{mid}_02_fva.tsv")

    # gene deletions
    model = read_sbml_model(mpath)
    mid = model.id
    create_gene_deletion_file(model, results_dir / f"{mid}_03_gene_deletion.tsv")

    # reaction deletions
    model = read_sbml_model(mpath)
    mid = model.id
    create_reaction_deletion_file(model, results_dir / f"{mid}_04_reaction_deletion.tsv")


def create_objective_file(model: cobra.Model, path: Path) -> float:
    """ Creates TSV file with objective value.

    see https://cobrapy.readthedocs.io/en/latest/simulating.html
    :param model:
    :param path:
    :return:
    """
    print(f"Objective: {path}")
    # create data frame and store
    solution = model.optimize()
    print(solution)

    with open(path, "w") as f_out:
        f_out.write(str(solution.objective_value))

    return solution.objective_value


def create_fva_file(model: cobra.Model, path: Path) -> pd.DataFrame:
    """ Creates TSV file with minimum and maximum value of Flux variability analysis.

    see https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA
    :param model:
    :param path:
    :return:
    """
    print(f"FVA: {path}")
    # create data frame and store
    df = flux_variability_analysis(model, model.reactions)

    # clean DataFrame
    df_out = pd.DataFrame(
        {"reaction": df.index,
         "minimum": df.minimum,
         "maximum": df.maximum
         })
    df_out.index = range(len(df_out))
    print(df_out.head(10))

    df_out.to_csv(path, sep="\t", index=False)
    return df_out


def create_gene_deletion_file(model: cobra.Model, path: Path) -> pd.DataFrame:
    """ Creates TSV with results of gene deletion.

    https://cobrapy.readthedocs.io/en/latest/deletions.html
    :param model:
    :param path:
    :return:
    """
    print(f"Gene deletions: {path}")
    # create data frame and store
    df = single_gene_deletion(model, model.genes)

    # clean DataFrame
    df_out = pd.DataFrame(
        {"gene": [set(ids).pop() for ids in df.index],
         "value": df.growth,
         "status": df.status
         })
    df_out.index = range(len(df_out))
    print(df_out.head(10))

    df_out.to_csv(path, sep="\t", index=False)
    return df_out


def create_reaction_deletion_file(model, path) -> pd.DataFrame:
    """ Creates TSV with results of reaction deletion.

    https://cobrapy.readthedocs.io/en/latest/deletions.html
    :param model:
    :param path:
    :return:
    """
    print(f"Reaction deletions: {path}")
    # create data frame and store
    df = single_reaction_deletion(model, model.reactions)

    # clean DataFrame
    df_out = pd.DataFrame(
        {"reaction": [set(ids).pop() for ids in df.index],
         "value": df.growth,
         "status": df.status
         })
    df_out.index = range(len(df_out))
    print(df_out.head(10))

    df_out.to_csv(path, sep="\t", index=False)
    return df_out


def example_ecoli_core(results_dir):
    """Create example files for ecoli core."""
    model_path = Path(__file__).parent / "models" / "e_coli_core.xml"
    create_fbc_files(results_dir=results_dir, model_path=model_path)


def example_iJR904(results_dir):
    """Create example files for ecoli core."""
    model_path = Path(__file__).parent / "models" / "iJR904.xml.gz"
    create_fbc_files(results_dir=results_dir, model_path=model_path)


if __name__ == "__main__":
    results_dir = Path(__file__).parent / "results"
    example_ecoli_core(results_dir)
    example_iJR904(results_dir)


