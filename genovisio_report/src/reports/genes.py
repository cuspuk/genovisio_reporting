from dataclasses import dataclass

from genovisio_report.src import input_schemas


@dataclass
class GeneReport:
    genes: list[str]
    count: int

    @property
    def list(self) -> str:
        result: list[str] = []
        for gene in self.genes:
            result.append(
                f'<a href="https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene}" target=_blank>{gene}</a>'
            )
            # TODO fix html being in python script, should be processed in template
        return ", ".join(result)


@dataclass
class GenesReport:
    protein_coding: int
    morbid: GeneReport
    disease: GeneReport
    hi: GeneReport
    ts: GeneReport

    @classmethod
    def build(cls, annot: input_schemas.AnnotationReporting) -> "GenesReport":
        return cls(
            protein_coding=annot.protein_coding_genes_count,
            morbid=GeneReport(genes=annot.morbid_genes, count=annot.morbid_genes_count),
            disease=GeneReport(genes=annot.disease_associated_genes, count=annot.disease_associated_genes_count),
            hi=GeneReport(genes=annot.hi_genes, count=annot.hi_genes_count),
            ts=GeneReport(genes=annot.ts_genes, count=annot.ts_genes_count),
        )
