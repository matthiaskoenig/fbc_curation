"""Command line tool `runfrog` for creating FROG reports."""
from pathlib import Path

from pymetadata import log
from pymetadata.console import console

from fbc_curation import __citation__, __version__
from fbc_curation.compare import FrogComparison
from fbc_curation.worker import run_frog


logger = log.get_logger(__name__)


def main() -> None:
    """Entry point which runs FROG report script.

    The script is registered as `runfrog` command.

    Example:
        runfrog --input resources/examples/models/e_coli_core.xml
          --output resources/examples/results/e_coli_core.omex
        python runfrog.py --input resources/examples/models/e_coli_core.xml
          --path resources/examples/results/e_coli_core.omex

    """

    import optparse
    import sys

    parser = optparse.OptionParser()
    parser.add_option(
        "-i",
        "--input",
        action="store",
        dest="input_path",
        help="(required) path to COMBINE archive (OMEX) with SBML model or "
        "an SBML model",
    )
    parser.add_option(
        "-o",
        "--output",
        action="store",
        dest="output_path",
        help="(required) omex output path to write FROG",
    )
    # parser.add_option(
    #     "-r",
    #     "--reference",
    #     action="store",
    #     dest="reference_path",
    #     help="(optional) path to COMBINE archive (OMEX) with FROG results "
    #     "to include in comparison",
    # )

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
            f"--output '{options.input_path}' output path must end in '.omex'"
        )

    # reference_path: Optional[Path] = None
    # if options.reference_path:
    #     reference_path = Path(options.reference_path)
    #     if not reference_path.exists():
    #         _parser_message(
    #             f"--reference '{options.reference_path}' does not exist, ensure "
    #             f"valid reference path."
    #         )

    run_frog(
        source_path=input_path,
        omex_path=output_path,
    )

    model_reports = FrogComparison.read_reports_from_omex(omex_path=output_path)
    for _, reports in model_reports.items():
        FrogComparison.compare_reports(reports=reports)


if __name__ == "__main__":
    main()
