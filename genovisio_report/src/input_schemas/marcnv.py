import pydantic

from genovisio_report.src import enums, input_utils


class MarcnvCriterion(pydantic.BaseModel):
    section: int
    option: str
    score: float | None = None
    reason: list[str]
    evidence: str

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
    def handle_marcnv_severity(cls, v: str) -> enums.Severity:
        # marcnv gives severity in lowercase
        v = v.upper()

        # handle special case of marcnv - "Uncertain"
        if v == "UNCERTAIN":
            return enums.Severity.VARIANT_OF_UNCERTAIN_SIGNIFICANCE
        return enums.Severity(v)

    @classmethod
    def construct_from_json_file(cls, path: str) -> "MarcNV":
        return cls(**input_utils.load_json_from_path(path))
