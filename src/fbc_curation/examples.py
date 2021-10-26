"""Create curation information for example models."""
from pathlib import Path
from typing import Dict

from pymetadata.console import console

from pymetadata.omex import Omex, EntryFormat, ManifestEntry

from fbc_curation import EXAMPLE_PATH
from fbc_curation.frog import FrogReport, CuratorConstants, FrogFormat
from fbc_curation.curator import Curator
from fbc_curation.curator.cameo_curator import CuratorCameo
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy


def run_examples(results_path: Path = EXAMPLE_PATH / "results"):
    """Run all examples."""
    example_ecoli_core(results_path=results_path / "e_coli_core")
    example_iJR904(results_path=results_path / "iJR904")
    example_iAB_AMO1410_SARS(results_path=results_path / "iAB_AMO1410_SARS")


def example_ecoli_core(results_path: Path) -> Dict:
    """Create FROG report for ecoli core."""
    return _run_example(
        EXAMPLE_PATH / "models" / "e_coli_core.xml", results_path=results_path
    )


def example_ecoli_core_omex(results_path: Path) -> Dict:
    """Create FROG report for ecoli core."""
    return _run_example(
        EXAMPLE_PATH / "models" / "e_coli_core.omex", results_path=results_path
    )


def example_iJR904(results_path: Path) -> Dict:
    """Create FROG report for iJR904."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iJR904.xml", results_path=results_path
    )


def example_iJR904_omex(results_path: Path) -> Dict:
    """Create FROG report for iJR904."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iJR904.omex", results_path=results_path
    )


def example_iAB_AMO1410_SARS(results_path: Path) -> Dict:
    """Create FROG report for iAB_AMO1410_SARS."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iAB_AMO1410_SARS-CoV-2.xml",
        results_path=results_path,
    )


def example_iAB_AMO1410_SARS_omex(results_path: Path) -> Dict:
    """Create FROG report for iAB_AMO1410_SARS."""
    return _run_example(
        EXAMPLE_PATH / "models" / "iAB_AMO1410_SARS-CoV-2.omex",
        results_path=results_path,
    )



def _run_example(model_path: Path, results_path: Path) -> Dict:
    console.rule(str(model_path))
    obj_info = Curator._read_objective_information(model_path)

    # Create FROG reports
    curator_keys = ["cobrapy", "cameo"]
    for k, curator_class in enumerate([CuratorCobrapy, CuratorCameo]):
        curator = curator_class(
            model_path=model_path, objective_id=obj_info.active_objective
        )
        report: FrogReport = curator.run()
        json_path = results_path / curator_keys[k] / CuratorConstants.REPORT_FILENAME
        report.to_json(json_path)

        # write tsv
        report.to_tsvs_with_metadata(results_path / curator_keys[k])

        # create omex
        omex = Omex()
        omex.add_entry(
            entry_path=model_path,
            entry=ManifestEntry(
                location=f"./{model_path.name}",
                format=EntryFormat.SBML,
            )
        )
        for curator_key in curator_keys:
            omex.add_entry(
                entry_path=json_path,
                entry=ManifestEntry(
                    location=f"./FROG/{curator_key}/{CuratorConstants.REPORT_FILENAME}",
                    format=FrogFormat.FROG_JSON_VERSION_1,
                )
            )
            for filename, format in [
                (
                    CuratorConstants.METADATA_FILENAME,
                    FrogFormat.FROG_METADATA_VERSION_1),
                (CuratorConstants.OBJECTIVE_FILENAME,
                 FrogFormat.FROG_OBJECTIVE_VERSION_1),
                (CuratorConstants.FVA_FILENAME, FrogFormat.FROG_FVA_VERSION_1),
                (CuratorConstants.REACTION_DELETION_FILENAME,
                 FrogFormat.FROG_REACTIONDELETION_VERSION_1),
                (CuratorConstants.GENE_DELETION_FILENAME,
                 FrogFormat.FROG_GENEDELETION_VERSION_1),
            ]:
                omex.add_entry(
                    entry_path=results_path / curator_keys[k] / filename,
                    entry=ManifestEntry(
                        location=f"./FROG/{curator_key}/{filename}",
                        format=format,
                    )
                )

    omex_path = results_path / f"{model_path.stem}_FROG.omex"
    omex.to_omex(omex_path)
    console.print(f"FROG OMEX written: 'file://{omex_path}'")


    # FIXME: reading and comparison
    # Read all reports
    # all_results: Dict[str: FrogReport] = {}
    # for curator_key in curator_keys:
    #     all_results[curator_key] = FrogReport.read_json(
    #         path=results_path / curator_key / CuratorConstants.REPORT_FILENAME
    #     )

    # comparison
    # valid = [r.validate() for r in all_results.values()]
    # equal = FrogReport.compare(all_results)
    # info = {
    #     "model_path": model_path,
    #     "valid": valid,
    #     "equal": equal,
    # }
    # console.print(info)
    # return info


if __name__ == "__main__":
    # run_examples()
    example_ecoli_core(results_path=EXAMPLE_PATH / "results" / "e_coli_core")
