#!/bin/sh
"""
Module for creating FBC curation files.
"""
import logging
from pathlib import Path
from pyfiglet import Figlet

from fbc_curation import __version__
from fbc_curation.curator import Curator, CuratorResults
logger = logging.getLogger(__name__)


def main():
    """
     Example:
         python curation.py --model ../examples/models/e_coli_core.xml --path ../examples/results/e_coli_core
         fbc_curation --model examples/models/e_coli_core.xml --path examples/results/e_coli_core
     """
    import sys
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-m', '--model',
                      action="store", dest="model_path",
                      help="(required) path to SBML model with fbc information")
    parser.add_option('-p', '--path',
                      action="store", dest="output_path",
                      help="(required) directory path to write output files to")
    parser.add_option('-c', '--curator',
                      action="store", dest="curator",
                      help="(optional) curator tool to create reference files: Select from ['cobrapy', 'cameo', 'all']")
    parser.add_option('-o', '--objective',
                      action="store", dest="objective",
                      help="(optional) objective to use in optimization, defaults to active objective")

    f = Figlet(font='slant')
    print(f.renderText('FBC CURATION'))
    print(f"Version {__version__} (https://github.com/matthiaskoenig/fbc_curation)\n")

    options, args = parser.parse_args()

    def _parser_message(text):
        print(text)
        parser.print_help()
        sys.exit(1)

    if not options.model_path:
        _parser_message("Required argument '--model' missing")
    if not options.output_path:
        _parser_message("Required argument '--path' missing")

    model_path = Path(options.model_path)
    if not model_path.exists():
        _parser_message(f"--model '{options.model_path}' does not exist, ensure valid model path.")

    output_path = Path(options.output_path)
    if not output_path.exists():
        logger.warning(f"output path --path '{output_path}' does not exist, path will be created.")

    if not options.curator:
        options.curator = "all"
    supported_curators = ["cameo", "cobrapy", "all"]
    if not options.curator in supported_curators:
        _parser_message(f"--curator '{options.curator}' is not supported, use one of the supported "
                        f"curators: {supported_curators}")

    obj_info = Curator.read_objective_information(model_path)
    if not options.objective:
        objective_id = obj_info.active_objective
    else:
        objective_id = options.objective
        if not objective_id in obj_info.objective_ids:
            _parser_message(f"Objective --objective'{objective_id}' dose not exist "
                            f"in SBML model objectives: "
                            f"'{obj_info.objective_ids}'")
        elif not objective_id == obj_info.active_objective:
            _parser_message(f"Only active_objective supported in cobrapy, use "
                            f"--objective {obj_info.active_objective}")

    # Perform imports here to avoid messages above parser messages
    output_paths = [output_path]
    if options.curator == "cobrapy":
        from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
        curator_classes = [CuratorCobrapy]
    elif options.curator == "cameo":
        from fbc_curation.curator.cameo_curator import CuratorCameo
        curator_classes = [CuratorCameo]
    elif options.curator == "all":
        from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
        from fbc_curation.curator.cameo_curator import CuratorCameo
        curator_classes = [CuratorCobrapy, CuratorCameo]
        output_paths = [output_path / "cobrapy", output_path / "cameo"]

    for k, curator_class in enumerate(curator_classes):
        curator = curator_class(model_path=model_path, objective_id=objective_id)
        results = curator.run()  # type: CuratorResults
        results.write_results(output_paths[k])


if __name__ == "__main__":
    main()
