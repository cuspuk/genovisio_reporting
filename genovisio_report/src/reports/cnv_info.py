from dataclasses import dataclass

from genovisio_report.src import input_schemas


@dataclass
class CNVInfo:
    type: str
    pos: str

    @classmethod
    def build(cls, cnv_data: input_schemas.AnnotationCNV) -> "CNVInfo":
        return cls(
            type=cnv_data.cnv_type.upper(),
            pos=f"{cnv_data.chrom_position}({cnv_data.chromosome}:{cnv_data.start}-{cnv_data.end})x{cnv_data.copy_number}",
        )
