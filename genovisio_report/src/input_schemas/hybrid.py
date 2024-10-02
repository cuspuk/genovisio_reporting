import pydantic

from genovisio_report.src import enums, input_utils


class HybridData(pydantic.BaseModel):
    score: float
    classification: enums.Severity

    @classmethod
    def construct_from_json_file(cls, path: str) -> "HybridData":
        return cls(**input_utils.load_json_from_path(path))
