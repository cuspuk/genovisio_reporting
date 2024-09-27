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
    protein_coding: GeneReport
    morbid: GeneReport
    disease: GeneReport
    hi: GeneReport
    ts: GeneReport

    @classmethod
    def build(cls, annot_data: input_schemas.Annotation) -> "GenesReport":
        return cls(
            protein_coding=GeneReport(
                genes=annot_data.genes.protein_coding_genes, count=annot_data.counters.protein_coding
            ),
            morbid=GeneReport(genes=annot_data.genes.morbid_genes, count=annot_data.counters.morbid_genes),
            disease=GeneReport(
                genes=annot_data.genes.disease_associated_genes, count=annot_data.counters.disease_associated_genes
            ),
            hi=GeneReport(genes=annot_data.genes.hi_genes, count=annot_data.counters.hi_genes),
            ts=GeneReport(genes=annot_data.genes.ts_genes, count=annot_data.counters.ts_genes),
        )
