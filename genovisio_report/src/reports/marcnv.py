from dataclasses import dataclass

from genovisio_report.src import input_schemas


@dataclass
class MarcNVReportSection:
    reasons: list[str]
    score: float | None = None

    @classmethod
    def create_from_criterion(cls, criterion: input_schemas.MarcnvCriterion) -> "MarcNVReportSection":
        if criterion.option != "Other":
            reasons = [f"<b>{criterion.option}.</b> {criterion.reason[0]}"]
        else:
            reasons = criterion.reason
        score = criterion.score
        return cls(reasons=reasons, score=score)


@dataclass
class MarcNVReport:
    Section_1: MarcNVReportSection
    Section_2: MarcNVReportSection
    Section_3: MarcNVReportSection
    Section_4: MarcNVReportSection
    Section_5: MarcNVReportSection

    @classmethod
    def build(cls, marcnv_data: input_schemas.MarcNV) -> "MarcNVReport":
        sections = {
            f"Section_{criterion.section}": MarcNVReportSection.create_from_criterion(criterion)
            for criterion in marcnv_data.criteria
        }
        return cls(**sections)
