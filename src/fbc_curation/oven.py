import tempfile
from math import isnan
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
import json
import orjson
from pathlib import Path
from rich import print
import numpy as np

class BaseModel(PydanticBaseModel):
    pass
    # @validator('*')
    # def change_nan_to_none(cls, v, field):
    #     if field.outer_type_ is float and isnan(v):
    #         return None
    #     return v


class Model(BaseModel):
    a: Optional[float] = None
    b: float

    # @validator('a')
    # def a_is_some(cls, v):
    #     print("v=", v)
    #     if v is None:
    #         return v
    #     return float(v)

models = [
    Model(a=None, b=3.1),
    Model(a=float('nan'), b=3.1),
    Model(a=np.NaN, b=3.1),
]
model2 =
print(repr(model))




with tempfile.TemporaryDirectory() as tmp_dir:
    json_path = Path(tmp_dir) / "example.json"
    with open(json_path, "w") as f_json:
        print(model.json())
        # f_json.write(model.json())

        json_str = orjson.dumps(model.dict()).decode("utf-8")
        print(json_str)
        f_json.write(
            json_str
        )




    with open(json_path, "r") as f_json:
        d = json.load(f_json)
        print(d)
        model2 = Model(**d)
