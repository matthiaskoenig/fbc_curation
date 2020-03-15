#!/bin/sh
"""
Module for creating FBC curation files via cobrapy.

Uses GLPK as default solver.
"""
from typing import List, Dict
import logging
import pandas as pd
import cobra
from cobra.io import read_sbml_model
from pathlib import Path
import libsbml

from cobra.flux_analysis import flux_variability_analysis
from cobra.flux_analysis import single_gene_deletion, single_reaction_deletion

logger = logging.getLogger(__file__)


class FBCFileCreator(object):
    """Class for creating refernce files for SBML curation."""
    NUM_DECIMALS = 8  # decimals to write in the solution

    # file namses for output files
    NAME_OBJECTIVE_FILE = "01_objective"
    NAME_FVA_FILE = "02_fva"
    NAME_GENE_DELETION_FILE = "03_gene_deletion"
    NAME_REACTION_DELETION_FILE = "04_reaction_deletion"

    def __init__(self, model_path: Path, results_dir: Path, num_decimals: int=None):
        self.model_path = model_path
        self.results_dir = results_dir,
        if not num_decimals:
            num_decimals = FBCFileCreator.NUM_DECIMALS
        self.num_decimals = num_decimals
        self.objective_id = None

    @staticmethod
    def _print_header(title):
        print()
        print("-" * 80)
        print(title)
        print("-" * 80)

    def create_fbc_files(self) -> pd.DataFrame:
        """ Creates all FBC curation files

        Model is reloaded for different files to make sure
        simulations are run from the initial model state.

        :param model_path:
        :param results_dir:
        :return:
        """
        # read objective information
        obj_dict = self.read_objective_information()
        self.objective_id = obj_dict["active_objective"]

        # objective value
        self.create_objective_file()

        # flux variability
        self.create_fva_file()

        # gene deletions
        self.create_gene_deletion_file()

        # reaction deletions
        self.create_reaction_deletion_file()


    def read_objective_information(self) -> Dict:
        """ Reads objective information from SBML file structure

        :param model_path:
        :return:
        """
        # read objective information from sbml (multiple objectives)
        doc = libsbml.readSBMLFromFile(str(self.model_path))  # type: libsbml.SBMLDocument
        model = doc.getModel()  # type: libsbml.Model
        fbc_model = model.getPlugin("fbc")  # type: libsbml.FbcModelPlugin
        active_objective = fbc_model.getActiveObjective()  # type: libsbml.Objective
        objective_ids = []
        for objective in fbc_model.getListOfObjectives():  # type: libsbml.Objective
            objective_ids.append(objective.getId())

        if len(objective_ids) > 1:
            logger.warnings(f"Multiple objectives exist in SBML-fbc ({objective_ids}), "
                            f"only active objective '{active_objective}' results "
                            f"are reported")
        return {
            'active_objective': active_objective,
            'objective_ids': objective_ids
        }

    def read_cobra_model(self) -> cobra.Model:
        """Loads and returns cobra model.

        :param model_path:
        :return:
        """
        mpath = str(self.path)
        return read_sbml_model(mpath)  # type: cobra.Model

    def create_objective_file(self) -> float:
        """ Creates TSV file with objective value.

        see https://cobrapy.readthedocs.io/en/latest/simulating.html
        :param model:
        :param path:
        :return:
        """
        path = self.results_dir / FBCFileCreator.NAME_OBJECTIVE_FILE
        self._print_header(f"Objective: {path}")
        model = self.read_cobra_model()  # type: cobra.Model

        # fbc optimization
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


    def main():
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

if __name__ == "__main__":
    main()
