import json

import pydantic

from genovisio_report.src import enums


class MarcnvCriterion(pydantic.BaseModel):
    section: int
    option: str
    score: float | None = None
    reason: list[str]

    @pydantic.field_validator("reason", mode="before")
    def reason_must_be_list(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [v]
        return v


class MarcNV(pydantic.BaseModel):
    score: float
    severity: enums.Severity
    criteria: list[MarcnvCriterion]

    @pydantic.field_validator("criteria", mode="after")
    def criteria_must_be_sorted(cls, v: list[MarcnvCriterion]) -> list[MarcnvCriterion]:
        return sorted(v, key=lambda x: x.section)

    @pydantic.field_validator("severity", mode="before")
    def check_VUS_severity(cls, v: str) -> enums.Severity:
        if v == "VUS":
            return enums.Severity.VARIANT_OF_UNCERTAIN_SIGNIFICANCE
        return enums.Severity(v)

    @classmethod
    def construct_from_json_file(cls, path: str) -> "MarcNV":
        with open(path, "r") as f:
            marcnv_input = json.load(f)
        return cls(**marcnv_input)
