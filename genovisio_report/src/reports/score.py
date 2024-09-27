from dataclasses import dataclass

from genovisio_report.src import enums, input_schemas


@dataclass
class ScoreReport:
    marcnv: float
    isv: float
    hybrid: float
    classification: enums.Severity

    @classmethod
    def build(
        cls, marcnv_data: input_schemas.MarcNV, isv_data: input_schemas.ISVResult, hybrid_data: input_schemas.HybridData
    ) -> "ScoreReport":
        return cls(
            marcnv=marcnv_data.score,
            isv=isv_data.score,
            hybrid=hybrid_data.score,
            classification=hybrid_data.classification,
        )
