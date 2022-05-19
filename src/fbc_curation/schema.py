"""Schema generation.

Code for creating JSON schema using pydantic.
https://json-schema.org/
"""
from pymetadata.console import console

from fbc_curation import FROG_SCHEMA_VERSION_1
from fbc_curation.frog import FrogReport


if __name__ == "__main__":
    console.rule(style="white")
    console.print(FrogReport.schema_json(indent=2))
    console.rule(style="white")
    with open(FROG_SCHEMA_VERSION_1, "w") as f_schema:
        f_schema.write(FrogReport.schema_json(indent=2))
