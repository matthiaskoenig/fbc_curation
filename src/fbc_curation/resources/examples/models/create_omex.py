from pathlib import Path

from pymetadata.console import console
from pymetadata.omex import EntryFormat, ManifestEntry, Omex

from fbc_curation import RESOURCES_DIR


if __name__ == "__main__":
    for example in ["e_coli_core.xml", "iAB_AMO1410_SARS-CoV-2.xml", "iJR904.xml"]:
        model_path: Path = RESOURCES_DIR / "examples" / "models" / example
        omex = Omex()
        omex.add_entry(
            entry_path=model_path,
            entry=ManifestEntry(
                location=f"./{example}", format=EntryFormat.SBML, master=True
            ),
        )
        omex_path = model_path.parent / f"{model_path.stem}.omex"
        console.log(omex_path)
        omex.to_omex(omex_path=omex_path)
