#!/bin/sh
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

NUM_DECIMALS = 8  # decimals to write in the solution


def print_header(title):
    print()
    print("-" * 80)
    print(title)
    print("-" * 80)


def create_fbc_files(model_path: Path, results_dir, decimals=NUM_DECIMALS) -> pd.DataFrame:
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
    create_objective_file(model, results_dir / f"{mid}_01_objective.tsv",
                          decimals=decimals)

    # flux variability
    mpath = str(model_path)
    model = read_sbml_model(mpath)
    mid = model.id
    create_fva_file(model, results_dir / f"{mid}_02_fva.tsv",
                    decimals=decimals)

    # gene deletions
    model = read_sbml_model(mpath)
    mid = model.id
    create_gene_deletion_file(model, results_dir / f"{mid}_03_gene_deletion.tsv",
                              decimals=decimals)

    # reaction deletions
    model = read_sbml_model(mpath)
    mid = model.id
    create_reaction_deletion_file(model, results_dir / f"{mid}_04_reaction_deletion.tsv",
                                  decimals=decimals)


def create_objective_file(model: cobra.Model, path: Path, decimals: int=NUM_DECIMALS) -> float:
    """ Creates TSV file with objective value.

    see https://cobrapy.readthedocs.io/en/latest/simulating.html
    :param model:
    :param path:
    :return:
    """
    print_header(f"Objective: {path}")
    # create data frame and store
    solution = model.optimize()
    print(solution)
    obj_value = round(solution.objective_value, NUM_DECIMALS)

    with open(path, "w") as f_out:
        f_out.write(str(obj_value))

    return obj_value


def create_fva_file(model: cobra.Model, path: Path, decimals: int=NUM_DECIMALS) -> pd.DataFrame:
    """ Creates TSV file with minimum and maximum value of Flux variability analysis.

    see https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA
    :param model:
    :param path:
    :return:
    """
    print_header(f"FVA: {path}")
    # create data frame and store
    df = flux_variability_analysis(model, model.reactions)

    # clean DataFrame
    df_out = pd.DataFrame(
        {"reaction": df.index,
         "minimum": df.minimum,
         "maximum": df.maximum
         })
    for key in ["minimum", "maximum"]:
        df_out[key] = df_out[key].apply(lambda x: round(x, decimals))
    df_out.sort_values(by=['reaction'], inplace=True)
    df_out.index = range(len(df_out))
    print(df_out.head(10))
    print('...')

    df_out.to_csv(path, sep="\t", index=False)
    return df_out


def create_gene_deletion_file(model: cobra.Model, path: Path,
                              decimals: int=NUM_DECIMALS) -> pd.DataFrame:
    """ Creates TSV with results of gene deletion.

    https://cobrapy.readthedocs.io/en/latest/deletions.html
    :param model:
    :param path:
    :return:
    """
    print_header(f"Gene deletions: {path}")
    # create data frame and store
    df = single_gene_deletion(model, model.genes)

    # clean DataFrame
    df_out = pd.DataFrame(
        {"gene": [set(ids).pop() for ids in df.index],
         "value": df.growth,
         "status": df.status
         })
    df_out.index = range(len(df_out))
    for key in ["value"]:
        df_out[key] = df_out[key].apply(lambda x: round(x, decimals)).abs()  # abs fixes the -0.0 | +0.0 diffs
    df_out.sort_values(by=['gene'], inplace=True)
    print(df_out.head(10))
    print('...')

    df_out.to_csv(path, sep="\t", index=False)
    return df_out


def create_reaction_deletion_file(model: cobra.Model, path: Path,
                                  decimals: int=NUM_DECIMALS) -> pd.DataFrame:
    """ Creates TSV with results of reaction deletion.

    https://cobrapy.readthedocs.io/en/latest/deletions.html
    :param model:
    :param path:
    :return:
    """
    print_header(f"Reaction deletions: {path}")
    # create data frame and store
    df = single_reaction_deletion(model, model.reactions)

    # clean DataFrame
    df_out = pd.DataFrame(
        {"reaction": [set(ids).pop() for ids in df.index],
         "value": df.growth,
         "status": df.status
         })
    df_out.sort_values(by=['reaction'], inplace=True)
    for key in ["value"]:
        df_out[key] = df_out[key].apply(lambda x: round(x, decimals)).abs()  # abs fixes the -0.0 | +0.0 diffs
    df_out.index = range(len(df_out))
    print(df_out.head(10))
    print('...')

    df_out.to_csv(path, sep="\t", index=False)
    return df_out


if __name__ == "__main__":
    """
    Example: 
        python fbc_curation.py --model ./models/e_coli_core.xml --out ./results
    """
    import sys
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-m', '--model',
                      action="store", dest="model_path",
                      help="path to SBML model with fbc information")
    parser.add_option('-o', '--out',
                      action="store", dest="output_path",
                      help="path to write the output to")

    options, args = parser.parse_args()

    if not options.model_path:
        print("Required argument '--model' missing")
        parser.print_help()
        sys.exit(1)
    if not options.output_path:
        print("Required argument '--out' missing")
        parser.print_help()
        sys.exit(1)

    model_path = Path(options.model_path)
    output_path = Path(options.output_path)
    create_fbc_files(results_dir=output_path, model_path=model_path)
