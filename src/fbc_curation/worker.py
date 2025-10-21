"""Worker.

Here the tasks are defined.
"""

import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional, Type, Union

from pymetadata import log
from pymetadata.console import console
from pymetadata.omex import EntryFormat, ManifestEntry, Omex

from fbc_curation import FROG_PATH_PREFIX
from fbc_curation.curator import Curator
from fbc_curation.curator.cameo_curator import CuratorCameo
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
from fbc_curation.frog import FrogReport


logger = log.get_logger(__name__)


# storage of data on server, only relevant for server
FROG_STORAGE = "/frog_data"


def run_frog(source_path: Path, omex_path: Path) -> None:
    """Create FROG report for given SBML or OMEX source.

    This function creates the FROG report and stores the results with the
    model in a COMBINE archive.

    :param source_path: Path for SBML model to create FROG for, or a COMBINE archive
      (omex) which contains an SBML model.
    :param omex_path: Path for COMBINE archive (omex) with FROG results. The content
      of the file will be overwritten!
    """
    frog_task(
        source_path_str=str(source_path),
        omex_path_str=str(omex_path),
    )


def frog_task(
    source_path_str: str,
    omex_path_str: Optional[str] = None,
) -> Dict[str, Any]:
    """Run FROG task and create JSON for omex path.

    This function should not be called directly. Use the `run_frog` function
    instead. Path can be either Omex or an SBML file.

    :param omex_path_str: Path to OMEX for results.
    """
    logger.info(f"Loading '{source_path_str}'")

    omex_path = Path(source_path_str)
    if not omex_path.exists():
        raise IOError(f"Path does not exist: '{omex_path}'")
    if not omex_path.is_file():
        raise IOError(f"Path is not a file: '{omex_path}'")

    # move data for task

    if Omex.is_omex(omex_path):
        omex = Omex().from_omex(omex_path)
    else:
        # Path is SBML we create a new archive
        omex = Omex()
        omex.add_entry(
            entry_path=omex_path,
            entry=ManifestEntry(
                location=f"./{omex_path.name}", format=EntryFormat.SBML, master=True
            ),
        )

    content = {"manifest": omex.manifest.model_dump(), "frogs": {}}

    # Add FROG JSON for all SBML files
    entry: ManifestEntry
    for entry in omex.manifest.entries:
        if entry.is_sbml():
            # TODO: check that SBML model with FBC information

            report_dict = {}
            for curator_key in ["cobrapy", "cameo"]:
                sbml_path: Path = omex.get_path(entry.location)
                report: FrogReport = _frog_for_sbml(
                    source=sbml_path, curator_key=curator_key
                )

                # add FROG files to archive
                report.add_to_omex(
                    omex, location_prefix=f"./{FROG_PATH_PREFIX}/{curator_key}/"
                )

                # add JSON to response
                report_dict[curator_key] = report.model_dump()

            # store all reports for SBML entry
            content["frogs"][entry.location] = report_dict

    # save archive for download
    if not omex_path_str:
        raise ValueError(
            "The 'omex_path_str' argument must be set (if not executed "
            "within a celery Task)."
        )

    omex_path = Path(omex_path_str)
    console.rule("Write OMEX", style="white")
    omex.to_omex(omex_path=omex_path)

    return content


def _frog_for_sbml(source: Union[Path, str, bytes], curator_key: str) -> FrogReport:
    """Create FROGReport for given SBML source.

    Source is either path to SBML file or SBML string.
    """

    if isinstance(source, bytes):
        source = source.decode("utf-8")

    time_start = time.time()

    with tempfile.TemporaryDirectory() as f_tmp:
        if isinstance(source, Path):
            sbml_path = source
        elif isinstance(source, str):
            sbml_path = Path(f_tmp) / "model.sbml"
            with open(sbml_path, "w") as f_sbml:
                f_sbml.write(source)

        curator_class: Type[Curator]
        if curator_key == "cobrapy":
            curator_class = CuratorCobrapy
        elif curator_key == "cameo":
            curator_class = CuratorCameo
        else:
            raise ValueError(f"Unsupported curator: {curator_key}")

        curator: Curator = curator_class(
            model_path=sbml_path,
            frog_id=curator_key,
            curators=[],
        )
        report: FrogReport = curator.run()

    time_elapsed = round(time.time() - time_start, 3)
    logger.info(f"FROG created in '{time_elapsed}' [s]")

    return report
