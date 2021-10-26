import os
import tempfile
import time
from pathlib import Path
from typing import Dict, Any, Union

from celery import Celery
from pymetadata.omex import Omex, ManifestEntry, EntryFormat

from pymetadata.console import console
from pymetadata import log

from fbc_curation.curator import Curator
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy
from fbc_curation.frog import FrogReport

logger = log.get_logger(__name__)


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

# FIXME: ensure the tmp dir is deleted afterwards


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@celery.task(name="frog_task")
def frog_task(omex_path_str: str, tmp_path: bool = True) -> Dict[str, Any]:
    """Run FROG task and create JSON for omex path.

    Path can be either Omex or an SBML file.
    """
    logger.error(f"Loading content from: {omex_path_str}")

    try:
        omex_path = Path(omex_path_str)
        if not omex_path.exists():
            raise IOError(f"Path does not exist: '{omex_path}'")
        if not omex_path.is_file():
            raise IOError(f"Path is not a file: '{omex_path}'")

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
                sbml_path: Path = omex.get_path(entry.location)
                content["frogs"][entry.location] = json_for_sbml(
                    source=sbml_path
                )
        else:
            logger.error("No SBML file found in archive!")
    finally:
        # cleanup temporary files for celery
        if tmp_path:
            os.remove(omex_path_str)

    return content


def json_for_sbml(source: Union[Path, str, bytes]) -> Dict:
    """Create FROG JSON content for given SBML source.

    Source is either path to SBML file or SBML string.
    """

    if isinstance(source, bytes):
        source = source.decode("utf-8")

    time_start = time.time()
    frog_json = frog_json_for_sbml(source=source)
    time_elapsed = round(time.time() - time_start, 3)

    debug = False
    if debug:
        console.rule("Creating JSON FROG")
        console.print(frog_json)
        console.rule()

    logger.info(f"JSON created for in '{time_elapsed}'")

    return frog_json


def frog_json_for_sbml(source: Union[Path, str]) -> FrogReport:
    """Read model info from SBML."""

    with tempfile.TemporaryDirectory() as f_tmp:
        if isinstance(source, Path):
            sbml_path = source
        elif isinstance(source, str):
            sbml_path = Path(f_tmp) / "model.sbml"
            with open(sbml_path, "w") as f_sbml:
                f_sbml.write(source)

        # return SBMLDocumentInfo(doc=doc)
        # curator_keys = ["cobrapy", "cameo"]
        obj_info = Curator._read_objective_information(sbml_path)
        curator = CuratorCobrapy(
                model_path=sbml_path, objective_id=obj_info.active_objective
        )
        report: FrogReport = curator.run()
        return report.dict()
