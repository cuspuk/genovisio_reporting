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
        return f"<b><i>{self.label}</i></b><br><b>value:</b> {self.value}<br><b>SHAP value:</b> {self.shap}"


def generate_plot_as_json(isv: input_schemas.ISVResult, annotation: input_schemas.Annotation) -> str:
    data = [
        ShapData(
            "disease_associated_genes",
            isv.isv_shap_values.disease_associated_genes,
            annotation.counters.disease_associated_genes,
        ),
        ShapData("gencode_genes", isv.isv_shap_values.gencode_genes, annotation.counters.gencode_genes),
        ShapData("hi_genes", isv.isv_shap_values.hi_genes, annotation.counters.hi_genes),
        ShapData("lncrna", isv.isv_shap_values.lncrna, annotation.counters.lncrna),
        ShapData("mirna", isv.isv_shap_values.mirna, annotation.counters.mirna),
        ShapData("morbid_genes", isv.isv_shap_values.morbid_genes, annotation.counters.morbid_genes),
        ShapData("protein_coding", isv.isv_shap_values.protein_coding, annotation.counters.protein_coding),
        ShapData("pseudogenes", isv.isv_shap_values.pseudogenes, annotation.counters.pseudogenes),
        ShapData("regions_HI", isv.isv_shap_values.regions_HI, annotation.counters.regions_HI),
        ShapData("regions_TS", isv.isv_shap_values.regions_TS, annotation.counters.regions_TS),
        ShapData("regulatory", isv.isv_shap_values.regulatory, annotation.counters.regulatory),
        ShapData(
            "regulatory_DNase_I_hypersensitive_site",
            isv.isv_shap_values.regulatory_DNase_I_hypersensitive_site,
            annotation.counters.regulatory_DNase_I_hypersensitive_site,
        ),
        ShapData(
            "regulatory_TATA_box", isv.isv_shap_values.regulatory_TATA_box, annotation.counters.regulatory_TATA_box
        ),
        ShapData(
            "regulatory_enhancer", isv.isv_shap_values.regulatory_enhancer, annotation.counters.regulatory_enhancer
        ),
        ShapData(
            "regulatory_enhancer_blocking_element",
            isv.isv_shap_values.regulatory_enhancer_blocking_element,
            annotation.counters.regulatory_enhancer_blocking_element,
        ),
        ShapData(
            "regulatory_promoter", isv.isv_shap_values.regulatory_promoter, annotation.counters.regulatory_promoter
        ),
        ShapData(
            "regulatory_silencer", isv.isv_shap_values.regulatory_silencer, annotation.counters.regulatory_silencer
        ),
        ShapData(
            "regulatory_transcriptional_cis_regulatory_region",
            isv.isv_shap_values.regulatory_transcriptional_cis_regulatory_region,
            annotation.counters.regulatory_transcriptional_cis_regulatory_region,
        ),
        ShapData("rrna", isv.isv_shap_values.rrna, annotation.counters.rrna),
        ShapData("snrna", isv.isv_shap_values.snrna, annotation.counters.snrna),
        ShapData("ts_genes", isv.isv_shap_values.ts_genes, annotation.counters.ts_genes),
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
