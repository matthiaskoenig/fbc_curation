#!/bin/sh
"""
Module for creating FBC curation files via cobrapy.

Uses GLPK as default solver.
"""
from typing import List, Dict
import logging
import pandas as pd
import cobra
from cobra.io import read_sbml_model, write_sbml_model
from cobra.exceptions import OptimizationError
from pathlib import Path
import libsbml

from cobra.flux_analysis import flux_variability_analysis
from cobra.flux_analysis import single_gene_deletion, single_reaction_deletion

logger = logging.getLogger(__file__)


class FBCFileCreator(object):
    """Class for creating refernce files for SBML curation."""
    NUM_DECIMALS = 6  # decimals to write in the solution

    # default output filenames
    FILENAME_OBJECTIVE_FILE = "01_objective.tsv"
    FILENAME_FVA_FILE = "02_fva.tsv"
    FILENAME_GENE_DELETION_FILE = "03_gene_deletion.tsv"
    FILENAME_REACTION_DELETION_FILE = "04_reaction_deletion.tsv"

    STATUS_OPTIMAL = "optimal"
    STATUS_INFEASIBLE = "infeasible"

    def __init__(self, model_path: Path,
                 results_path: Path,
                 objective_id: str = None,
                 num_decimals: int = None):
        """

        :param model_path:
        :param results_path: directory where to write the output
        :param objective_id: id of objective to optimize, if no id is provided
            the active objective is used
        :param num_decimals: number of digits to round the solutions
        :return:
        """
        self.model_path = model_path
        self.results_path = results_path

        if not objective_id:
            obj_dict = self.read_objective_information(self.model_path)
            objective_id = obj_dict["active_objective"]
        self.objective_id = objective_id

        if not num_decimals:
            num_decimals = FBCFileCreator.NUM_DECIMALS
        self.num_decimals = num_decimals

        print(self)

        if not model_path.exists():
            raise ValueError(f"model_path does not exist: '{self.model_path}'")



    def __str__(self):
        lines = [
            f"--- {self.__class__.__name__} ---",
            f"\tmodel_path: {self.model_path}",
            f"\tresults_path: {self.results_path}",
            f"\tobjective_id: {self.objective_id}",
            f"\tnum_decimals: {self.num_decimals}",
        ]
        return "\n".join(lines)

    def create_fbc_files(self) -> pd.DataFrame:
        """ Creates all FBC curation files

        Model is reloaded for different files to make sure
        simulations are run from the initial model state.

        :param model_path:
        :param results_dir:
        :return:
        """
        # objective value
        self.create_objective_file()

        # flux variability
        self.create_fva_file()

        # gene deletions
        self.create_gene_deletion_file()

        # reaction deletions
        self.create_reaction_deletion_file()

    @staticmethod
    def read_objective_information(model_path) -> Dict:
        """ Reads objective information from SBML file structure

        :param model_path:
        :return:
        """
        # read objective information from sbml (multiple objectives)
        doc = libsbml.readSBMLFromFile(str(model_path))  # type: libsbml.SBMLDocument
        model = doc.getModel()  # type: libsbml.Model
        fbc_model = model.getPlugin("fbc")  # type: libsbml.FbcModelPlugin
        if fbc_model is None:
            # model is an old SBML model without fbc information (use cobra default)
            # problems with the automatic up-conversions
            active_objective = "obj"
            objective_ids = ["obj"]
        else:
            active_objective = fbc_model.getActiveObjective().getId()
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
        mpath = str(self.model_path)
        print(mpath)
        return read_sbml_model(mpath)  # type: cobra.Model

    @staticmethod
    def _print_header(title):
        print()
        print("-" * 80)
        print(title)
        print("-" * 80)

    def create_objective_file(self, filename: str=None) -> pd.DataFrame:
        """ Creates TSV file with objective value.

        see https://cobrapy.readthedocs.io/en/latest/simulating.html
        :param filename:
        :return:
        """
        if not filename:
            filename = FBCFileCreator.FILENAME_OBJECTIVE_FILE
        path = self.results_path / filename
        self._print_header(f"Objective: {path}")
        model = self.read_cobra_model()  # type: cobra.Model

        # fbc optimization
        value = None
        try:
            solution = model.optimize()
            value = solution.objective_value
            status = FBCFileCreator.STATUS_OPTIMAL
        except OptimizationError as e:
            logger.error(f"{e}")
            value = ''
            status = FBCFileCreator.STATUS_INFEASIBLE

        df_out = pd.DataFrame(
            {
                "model": model.id,
                "objective": [self.objective_id],
                "status": [status],
                "value": [value],
             })
        for key in ["value"]:
            df_out[key] = df_out[key].apply(lambda x: round(x, self.num_decimals))
        df_out.sort_values(by=['objective'], inplace=True)

        print(df_out.head(10))
        print('...')

        df_out.to_csv(path, sep="\t", index=False)

        return df_out

    def create_fva_file(self, filename: str=None) -> pd.DataFrame:
        """ Creates TSV file with minimum and maximum value of Flux variability analysis.

        see https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA
        :param filename:
        :return:
        """
        if not filename:
            filename = FBCFileCreator.FILENAME_FVA_FILE
        path = self.results_path / filename
        self._print_header(f"FVA: {path}")
        model = self.read_cobra_model()  # type: cobra.Model
        # create data frame and store
        try:
            df = flux_variability_analysis(model, model.reactions)

            # clean DataFrame
            df_out = pd.DataFrame(
                {
                    "model": model.id,
                    "objective": self.objective_id,
                    "reaction": df.index,
                    "status": FBCFileCreator.STATUS_OPTIMAL,
                    "minimum": df.minimum,
                    "maximum": df.maximum
                 })
            for key in ["minimum", "maximum"]:
                df_out[key] = df_out[key].apply(lambda x: round(x, self.num_decimals))
        except OptimizationError as e:
            logger.error(f"{e}")
            df_out = pd.DataFrame(
                {
                    "model": model.id,
                    "objective": self.objective_id,
                    "reaction": [r.id for r in model.reactions],
                    "status": FBCFileCreator.STATUS_INFEASIBLE,
                    "minimum": '',
                    "maximum": '',
                })

        df_out.sort_values(by=['reaction'], inplace=True)
        df_out.index = range(len(df_out))
        print(df_out.head(10))
        print('...')

        df_out.to_csv(path, sep="\t", index=False)
        return df_out

    def create_gene_deletion_file(self, filename: str=None) -> pd.DataFrame:
        """ Creates TSV with results of gene deletion.

        https://cobrapy.readthedocs.io/en/latest/deletions.html
        :param filename:
        :return:
        """
        if not filename:
            filename = FBCFileCreator.FILENAME_GENE_DELETION_FILE
        path = self.results_path / filename
        self._print_header(f"Gene deletions: {path}")
        model = self.read_cobra_model()  # type: cobra.Model

        # create data frame and store
        df = single_gene_deletion(model, model.genes)

        # clean DataFrame
        df_out = pd.DataFrame(
            {
                "model": model.id,
                "objective": self.objective_id,
                "gene": [set(ids).pop() for ids in df.index],
                "status": df.status,
                "value": df.growth,
             })
        df_out.index = range(len(df_out))
        for key in ["value"]:
            df_out[key] = df_out[key].apply(lambda x: round(x, self.num_decimals)).abs()  # abs fixes the -0.0 | +0.0 diffs
        df_out.sort_values(by=['gene'], inplace=True)
        print(df_out.head(10))
        print('...')

        df_out.to_csv(path, sep="\t", index=False)
        return df_out

    def create_reaction_deletion_file(self, filename: str=None) -> pd.DataFrame:
        """ Creates TSV with results of reaction deletion.

        https://cobrapy.readthedocs.io/en/latest/deletions.html
        :param filename:
        :return:
        """
        if not filename:
            filename = FBCFileCreator.FILENAME_REACTION_DELETION_FILE
        path = self.results_path / filename
        self._print_header(f"Reaction deletions: {path}")
        # create data frame and store
        model = self.read_cobra_model()  # type: cobra.Model
        df = single_reaction_deletion(model, model.reactions)

        # clean DataFrame
        df_out = pd.DataFrame(
            {
                "model": model.id,
                "objective": self.objective_id,
                "reaction": [set(ids).pop() for ids in df.index],
                "status": df.status,
                "value": df.growth,
             })
        df_out.sort_values(by=['reaction'], inplace=True)
        for key in ["value"]:
            df_out[key] = df_out[key].apply(lambda x: round(x, self.num_decimals)).abs()  # abs fixes the -0.0 | +0.0 diffs
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
    parser.add_option('-p', '--path',
                      action="store", dest="output_path",
                      help="path to write the files to (directory)")
    parser.add_option('-o', '--objective',
                      action="store", dest="objective",
                      help="optional objective to use in optimization")

    options, args = parser.parse_args()

    def _parser_message(text):
        print(text)
        parser.print_help()
        sys.exit(1)

    if not options.model_path:
        _parser_message("Required argument '--model' missing")
    if not options.output_path:
        _parser_message("Required argument '--out' missing")

    model_path = Path(options.model_path)
    output_path = Path(options.output_path)

    obj_dict = FBCFileCreator.read_objective_information(model_path)
    if not options.objective:
        objective_id = obj_dict['active_objective']
    else:
        objective_id = options.objective
        if not objective_id in obj_dict['objective_ids']:
            _parser_message(f"Objective '{objective_id}' dose not exist "
                            f"in model objectives: "
                            f"'{obj_dict['objective_ids']}'")
        elif not objective_id == obj_dict['active_objective']:
            _parser_message(f"Only active_objective supported in cobrapy, use "
                            f"--objective {obj_dict['active_objective']}")

    file_creator = FBCFileCreator(
        model_path=model_path,
        results_path=output_path,
        objective_id=objective_id
    )
    file_creator.create_fbc_files()


if __name__ == "__main__":
    main()
