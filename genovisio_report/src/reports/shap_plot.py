import re
from dataclasses import dataclass

import plotly.graph_objects as go

from genovisio_report.src import input_schemas


def _split_string(s: str) -> str:
    words = s.split("_")
    result: list[str] = []
    current = words[0]
    for word in words[1:]:
        if len(current) + len(word) < 35:
            current += f"_{word}"
        else:
            result.append(current)
            current = word
    if current not in result:
        result.append(current)

    return "<br>".join(result)


@dataclass
class ShapData:
    name: str
    shap: float
    value: int

    @property
    def label(self) -> str:
        return f"[{self.value:.1f}] = {self.name}"

    @property
    def color_label(self) -> str | None:
        m = re.search(r"(\[.+\] = )(.+)", _split_string(self.label))
        if m:
            return f'<span style="color: gray;">{m.group(1)}</span>{m.group(2)}'
        return None

    @property
    def color(self) -> str:
        if self.shap > 0:
            return "rgb(225, 29, 29)"
        elif self.shap < 0:
            return "rgb(0, 128, 0)"
        else:
            return "gray"

    @property
    def hovertext(self) -> str:
        return f"<b><i>{self.name}</i></b><br><b>value:</b> {self.value}<br><b>SHAP value:</b> {self.shap}"


def generate_plot_as_json(isv: input_schemas.ISVResult, annotation: input_schemas.Annotation) -> str:
    data = [
        ShapData(
            "Disease associated Genes",
            isv.isv_shap_values.disease_associated_genes,
            annotation.counters.disease_associated_genes,
        ),
        ShapData("Overlapped Gencode Elements", isv.isv_shap_values.gencode_genes, annotation.counters.gencode_genes),
        ShapData("Haploinsufficient Genes", isv.isv_shap_values.hi_genes, annotation.counters.hi_genes),
        ShapData("Long non-coding RNA", isv.isv_shap_values.lncrna, annotation.counters.lncrna),
        ShapData("Micro RNA", isv.isv_shap_values.mirna, annotation.counters.mirna),
        ShapData("Morbid Genes", isv.isv_shap_values.morbid_genes, annotation.counters.morbid_genes),
        ShapData("Protein Coding Genes", isv.isv_shap_values.protein_coding, annotation.counters.protein_coding),
        ShapData("Pseudogenes", isv.isv_shap_values.pseudogenes, annotation.counters.pseudogenes),
        ShapData("Haploinsufficient Regions", isv.isv_shap_values.regions_HI, annotation.counters.regions_HI),
        ShapData("Triplosensitive Regions", isv.isv_shap_values.regions_TS, annotation.counters.regions_TS),
        ShapData("Regulatory Elements", isv.isv_shap_values.regulatory, annotation.counters.regulatory),
        ShapData(
            "DNase I hypersensitive sites",
            isv.isv_shap_values.regulatory_DNase_I_hypersensitive_site,
            annotation.counters.regulatory_DNase_I_hypersensitive_site,
        ),
        ShapData("TATA box", isv.isv_shap_values.regulatory_TATA_box, annotation.counters.regulatory_TATA_box),
        ShapData("Enhancers", isv.isv_shap_values.regulatory_enhancer, annotation.counters.regulatory_enhancer),
        ShapData(
            "Enhancer-blocking Elements",
            isv.isv_shap_values.regulatory_enhancer_blocking_element,
            annotation.counters.regulatory_enhancer_blocking_element,
        ),
        ShapData("Promoters", isv.isv_shap_values.regulatory_promoter, annotation.counters.regulatory_promoter),
        ShapData("Silencers", isv.isv_shap_values.regulatory_silencer, annotation.counters.regulatory_silencer),
        ShapData(
            "Transcriptional cis-regulatory Regions",
            isv.isv_shap_values.regulatory_transcriptional_cis_regulatory_region,
            annotation.counters.regulatory_transcriptional_cis_regulatory_region,
        ),
        ShapData("Ribosomal RNA", isv.isv_shap_values.rrna, annotation.counters.rrna),
        ShapData("Small nuclear RNA", isv.isv_shap_values.snrna, annotation.counters.snrna),
        ShapData("Triplosensitivity Genes", isv.isv_shap_values.ts_genes, annotation.counters.ts_genes),
    ]

    # sort data by name in reverse order
    data = sorted(data, key=lambda x: x.name, reverse=True)

    # Extract the data into separate lists
    labels = [dp.label for dp in data]
    colors = [dp.color for dp in data]
    hovertexts = [dp.hovertext for dp in data]
    shaps = [dp.shap for dp in data]
    color_labels = [dp.color_label for dp in data]

    fig = go.Figure()
    fig.add_bar(
        x=shaps,
        y=labels,
        orientation="h",
        marker=dict(color=colors),
        text=shaps,
        textposition="outside",
        textfont=dict(size=7),
        hovertext=hovertexts,
        hoverinfo="text",
    )

    fig.add_vline(x=0, line_color="black", line_width=1)
    fig.update_xaxes(tickfont=dict(size=7), range=[-1, 1])
    fig.update_yaxes(tickfont=dict(size=7), tickmode="array", tickvals=labels, ticktext=color_labels)
    fig.update_layout(template="plotly_white", height=450, width=400, margin=dict(l=20, r=20, t=20, b=20))
    return fig.to_json()
