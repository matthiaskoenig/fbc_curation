"""Module creates FBC curation files."""
from pathlib import Path
from typing import Dict, List, Type

from pymetadata import log
from pymetadata.console import console

from fbc_curation import __citation__, __version__
from fbc_curation.curator import Curator
from fbc_curation.frog import FrogReport
from fbc_curation.worker import frog_task


logger = log.get_logger(__name__)


def main() -> None:
    """Entry point which runs FROG report script.

    The script is registered as `runfrog`.

    Example:
        runfrog --input resources/examples/models/e_coli_core.xml --output resources/examples/results/e_coli_core.omex
        python runfrog.py --input resources/examples/models/e_coli_core.xml --path resources/examples/results/e_coli_core.omex

    """

    import optparse
    import sys

    parser = optparse.OptionParser()
    parser.add_option(
        "-i",
        "--input",
        action="store",
        dest="input_path",
        help="(required) path to OMEX with SBML model or SBML model with fbc information",
    )
    parser.add_option(
        "-o",
        "--output",
        action="store",
        dest="output_path",
        help="(required) omex output path to write FROG to with file ending '.omex'",
    )
    parser.add_option(
        "-r",
        "--reference",
        action="store",
        dest="reference_path",
        help="(optional) path to OMEX with FROG results to include in comparison",
    )

    console.rule(style="white")
    console.print(":frog: FBC CURATION FROG ANALYSIS :frog:")
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

    if not options.input_path:
        _parser_message("Required argument '--input' missing")
    if not options.output_path:
        _parser_message("Required argument '--output' missing")

    input_path = Path(options.input_path)
    if not input_path.exists():
        _parser_message(
            f"--input '{options.input_path}' does not exist, ensure valid model or "
            f"OMEX path."
        )

    output_path = Path(options.output_path)
    if not str(output_path).endswith(".omex"):
        _parser_message(
            f"--output '{options.model_path}' output path must end in '.omex'"
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

    frog_task(
        source_path_str=str(input_path),
        input_is_temporary=False,
        omex_path_str=str(output_path),
    )


    # TODO: comparison with reference solution
    # Reading reference solution
    # res_dict: Dict[str, FrogReport] = {}
    # if reference_path:
    #     reference_results = FrogReport.read_results(reference_path)
    #     res_dict["reference"] = reference_results
    #
    # for k, curator_class in enumerate(curator_classes):
    #     key = curator_keys[k]
    #     curator = curator_class(model_path=model_path, objective_id=objective_id)
    #     results = curator.run()  # type: FROGResults
    #     results.write_results(output_path / key)
    #     res_dict[key] = FrogReport.read_results(output_path / key)
    #
    # # perform comparison
    # if len(res_dict) > 1:
    #     FrogReport.compare(res_dict)


if __name__ == "__main__":
    main()
