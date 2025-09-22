"""Schema generation.

Code for creating JSON schema using pydantic.
https://json-schema.org/
"""
from orjson import orjson
from pymetadata.console import console

from fbc_curation import FROG_SCHEMA_VERSION_1
from fbc_curation.frog import FrogReport


if __name__ == "__main__":
    schema_dict = FrogReport.model_json_schema()
    console.rule(style="white")
    console.print(schema_dict)
    console.rule(style="white")

    with open(FROG_SCHEMA_VERSION_1, "w+b") as f_json:
        json_bytes = orjson.dumps(schema_dict, option=orjson.OPT_INDENT_2)
        f_json.write(json_bytes)
