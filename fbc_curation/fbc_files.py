#!/bin/sh
"""
Module for creating FBC curation files via cobrapy.

Uses GLPK as default solver.
"""


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
