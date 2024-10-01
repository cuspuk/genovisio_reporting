import json

import pydantic


class AnnotationCounters(pydantic.BaseModel):
    gencode_genes: int
    protein_coding: int
    pseudogenes: int
    mirna: int
    lncrna: int
    rrna: int
    snrna: int
    morbid_genes: int
    disease_associated_genes: int
    hi_genes: int
    ts_genes: int = 0  # TODO must be added
    regions_HI: int
    regions_TS: int
    regulatory: int
    regulatory_enhancer: int
    regulatory_silencer: int
    regulatory_transcriptional_cis_regulatory_region: int
    regulatory_promoter: int
    regulatory_DNase_I_hypersensitive_site: int
    regulatory_enhancer_blocking_element: int
    regulatory_TATA_box: int

    def as_dict(self) -> dict[str, int]:
        return self.model_dump()


class AnnotationReporting(pydantic.BaseModel):
    morbid_genes: list[str] = pydantic.Field(alias="morbid_genes")
    disease_associated_genes: list[str] = pydantic.Field(alias="disease_associated_genes")
    hi_genes: list[str] = pydantic.Field(alias="HI_genes")
    ts_genes: list[str] = pydantic.Field(alias="TS_genes")
    protein_coding_genes_count: int
    hi_genes_count: int = pydantic.Field(alias="HI_genes_count")
    ts_genes_count: int = pydantic.Field(alias="TS_genes_count")
    morbid_genes_count: int
    disease_associated_genes_count: int


class Annotation(pydantic.BaseModel):
    counters: AnnotationCounters = pydantic.Field(alias="isv_annot_values")
    genes: AnnotationReporting = pydantic.Field(alias="annotations_reporting")

    @classmethod
    def construct_from_json_file(cls, path: str) -> "Annotation":
        with open(path, "r") as f:
            annotation_input = json.load(f)
        return cls(**annotation_input)
