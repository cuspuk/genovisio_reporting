import json

import pydantic

from genovisio_report.src import enums


class HybridData(pydantic.BaseModel):
    score: float
    classification: enums.Severity

    @classmethod
    def construct_from_json_file(cls, path: str) -> "HybridData":
        with open(path, "r") as f:
            hybrid_input = json.load(f)
        return cls(**hybrid_input)
