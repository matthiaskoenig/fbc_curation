"""Module creates FBC curation files."""
from pathlib import Path
from typing import Dict, List, Type

from pymetadata import log
from pymetadata.console import console

from fbc_curation import __citation__, __version__
from fbc_curation.curator import Curator
from fbc_curation.frog import FrogReport


logger = log.get_logger(__name__)


def main() -> None:
    """Entry point which runs FROG report script.

    The script is registered as `runfrog`.

    Example:
        runfrog --model resources/examples/models/e_coli_core.xml
          --path resources/examples/results/e_coli_core

        python curation.py --model resources/examples/models/e_coli_core.xml
          --path resources/examples/results/e_coli_core

    """

    import optparse
    import sys

    parser = optparse.OptionParser()
    parser.add_option(
        "-m",
        "--model",
        action="store",
        dest="model_path",
        help="(required) path to SBML model with fbc information",
    )
    parser.add_option(
        "-p",
        "--path",
        action="store",
        dest="output_path",
        help="(required) directory path to write output files to",
    )
    parser.add_option(
        "-c",
        "--curator",
        action="store",
        dest="curator",
        help="(optional) curator tool to create reference files: Select from "
        "['cobrapy', 'cameo', 'all']",
    )
    parser.add_option(
        "-o",
        "--objective",
        action="store",
        dest="objective",
        help="(optional) objective to use in optimization, "
        "defaults to active objective",
    )
    parser.add_option(
        "-r",
        "--reference",
        action="store",
        dest="reference_path",
        help="(optional) directory path to reference output (comparison is performed)",
    )

    console.rule(style="white")
    console.print(":frog: FBC CURATION FROG ANALYSIS :frog:", style="white on black")
    console.print(
        f"Version {__version__} (https://github.com/matthiaskoenig/fbc_curation)"
    )
    console.print(f"Citation {__citation__}")
    console.rule(style="white")

    options, args = parser.parse_args()

    def _parser_message(text: str) -> None:
        console.print(text)
        parser.print_help()
        console.rule(style="white")
        sys.exit(1)

    if not options.model_path:
        _parser_message("Required argument '--model' missing")
    if not options.output_path:
        _parser_message("Required argument '--path' missing")

    model_path = Path(options.model_path)
    if not model_path.exists():
        _parser_message(
            f"--model '{options.model_path}' does not exist, ensure valid model path."
        )

    output_path = Path(options.output_path)
    if not output_path.exists():
        logger.warning(
            f"output path --path '{output_path}' does not exist, path will be created."
        )

    if not options.reference_path:
        reference_path = None
    else:
        reference_path = Path(options.reference_path)
        if not reference_path.exists():
            _parser_message(
                f"--reference '{options.reference_path}' does not exist, ensure "
                f"valid reference path."
            )

    if not options.curator:
        options.curator = "all"
    supported_curators = ["cameo", "cobrapy", "all"]
    if options.curator not in supported_curators:
        _parser_message(
            f"--curator '{options.curator}' is not supported, use one of the supported "
            f"curators: {supported_curators}"
        )

    obj_info = Curator._read_objective_information(model_path)
    if not options.objective:
        objective_id = obj_info.active_objective
    else:
        objective_id = options.objective
        if objective_id not in obj_info.objective_ids:
            _parser_message(
                f"Objective --objective'{objective_id}' dose not exist "
                f"in SBML model objectives: "
                f"'{obj_info.objective_ids}'"
            )
        elif not objective_id == obj_info.active_objective:
            _parser_message(
                f"Only active_objective supported in cobrapy, use "
                f"--objective {obj_info.active_objective}"
            )

    # Perform imports here to avoid messages above parser messages
    curator_classes: List[Type[Curator]]
    if options.curator == "cobrapy":
        from fbc_curation.curator.cobrapy_curator import CuratorCobrapy

        curator_classes = [CuratorCobrapy]
        curator_keys = ["cobrapy"]
    elif options.curator == "cameo":
        from fbc_curation.curator.cameo_curator import CuratorCameo

        curator_classes = [CuratorCameo]
        curator_keys = ["cameo"]
    elif options.curator == "all":
        from fbc_curation.curator.cameo_curator import CuratorCameo
        from fbc_curation.curator.cobrapy_curator import CuratorCobrapy

        curator_classes = [CuratorCobrapy, CuratorCameo]
        curator_keys = ["cobrapy", "cameo"]

    # Reading reference solution
    res_dict: Dict[str, FrogReport] = {}
    if reference_path:
        reference_results = FrogReport.read_results(reference_path)
        res_dict["reference"] = reference_results

    for k, curator_class in enumerate(curator_classes):
        key = curator_keys[k]
        curator = curator_class(model_path=model_path, objective_id=objective_id)
        results = curator.run()  # type: FROGResults
        results.write_results(output_path / key)
        res_dict[key] = FrogReport.read_results(output_path / key)

    # TODO: write to OMEX
    # FIXME: reuse the functionality

    # perform comparison
    if len(res_dict) > 1:
        FrogReport.compare(res_dict)


if __name__ == "__main__":
    main()
