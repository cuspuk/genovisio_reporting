import json

import pydantic

from genovisio_report.src import enums


class CNVRegion(pydantic.BaseModel):
    chromosome: str
    start: int
    end: int
    cnv_type: enums.CNVType
    chrom_position: str = pydantic.Field(alias="cytobands_desc")
    cytobands: list[str]

    @property
    def copy_number(self) -> int:
        return 1 if self.cnv_type == enums.CNVType.LOSS else 3

    @classmethod
    def construct_from_json_file(cls, path: str) -> "CNVRegion":
        with open(path, "r") as f:
            annotation_input = json.load(f)
        return cls(**annotation_input["cnv"])
