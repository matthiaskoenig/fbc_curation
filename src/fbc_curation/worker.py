"""Celery worker.

Here the tasks are defined which are executed in the task queue.
"""
import os
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional, Type, Union

from celery import Celery
from pymetadata import log
from pymetadata.console import console
from pymetadata.omex import EntryFormat, ManifestEntry, Omex

from fbc_curation.curator import Curator
from fbc_curation.curator.cameo_curator import CuratorCameo
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
from fbc_curation.frog import FrogReport


logger = log.get_logger(__name__)


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

# FIXME: ensure that files are removed from time to time


@celery.task(name="frog_task")
def frog_task(
    source_path_str: str,
    input_is_temporary: bool = True,
    omex_path_str: Optional[str] = None,
) -> Dict[str, Any]:
    """Run FROG task and create JSON for omex path.

    Path can be either Omex or an SBML file.
    """
    logger.info(f"Loading '{source_path_str}'")

    try:
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
                    location="./model.xml", format=EntryFormat.SBML, master=True
                ),
            )

        content = {"manifest": omex.manifest.dict(), "frogs": {}}

        # Add FROG JSON for all SBML files
        entry: ManifestEntry
        for entry in omex.manifest.entries:
            if entry.is_sbml():
                # TODO: check that SBML model with FBC information

                report_dict = {}
                for curator_key in ["cobrapy", "cameo"]:
                    sbml_path: Path = omex.get_path(entry.location)
                    report: FrogReport = frog_for_sbml(
                        source=sbml_path, curator_key=curator_key
                    )

                    # add FROG files to archive
                    report.add_to_omex(omex, location_prefix=f"./FROG/{curator_key}/")

                    # add JSON to response
                    report_dict[curator_key] = report.dict()

                # store all reports for SBML entry
                content["frogs"][entry.location] = report_dict

        # save archive for download
        if omex_path_str is None:
            # executed in task queue
            task_id = frog_task.request.id
            omex_path = Path("/frog_data") / f"{task_id}.omex"
        else:
            omex_path = Path(omex_path_str)
        console.rule("Write OMEX", style="white")
        omex.to_omex(omex_path=omex_path)

    finally:
        # cleanup temporary files for celery
        if input_is_temporary:
            os.remove(source_path_str)

    return content


def frog_for_sbml(source: Union[Path, str, bytes], curator_key: str) -> FrogReport:
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
