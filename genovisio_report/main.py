import argparse
import os
import sys

import jinja2

from genovisio_report.src import core, input_schemas, reports


def render_template_html(
    cnv_path: str, annot_path: str, marcnv_path: str, isv_path: str, hybrid_path: str, report_id: str | None
) -> str:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(core.TEMPLATES_DIR))
    template = env.get_template(core.TEMPLATE_FILENAME)

    with open(core.CSS_FILE, "r") as f:
        css = f.read()

    marcnv_data = input_schemas.MarcNV.construct_from_json_file(marcnv_path)
    hybrid_data = input_schemas.HybridData.construct_from_json_file(hybrid_path)
    annot_data = input_schemas.Annotation.construct_from_json_file(annot_path)
    isv_data = input_schemas.ISVResult.construct_from_json_file(isv_path)
    cnv_region = input_schemas.CNVRegion.construct_from_json_file(cnv_path)

    marcnv_report = reports.MarcNVReport.build(marcnv_data)
    score_report = reports.ScoreReport.build(marcnv_data, isv_data, hybrid_data)
    genes_report = reports.GenesReport.build(annot_data.genes)
    cnv_info = reports.CNVInfo.build(cnv_region)
    shap_plot_json = reports.generate_plot_as_json(isv_data, annot_data)

    content = template.render(
        css=css,
        id=report_id,
        cnv_info=cnv_info,
        scores=score_report,
        acmg=marcnv_report,
        isv_shap=shap_plot_json,
        genes=genes_report,
        marcnv_plot=reports.create_prediction_plot(marcnv_data.score, type="marcnv"),
        isv_plot=reports.create_prediction_plot(isv_data.score, type="isv"),
        hybrid_plot=reports.create_prediction_plot(hybrid_data.score, type="hybrid"),
        decimal_places=core.DECIMAL_PLACES,
    )

    return content


def genovisio_report(
    cnv_input: str,
    annotation_input: str,
    isv_input: str,
    marcnv_input: str,
    hybrid_input: str,
    output_html: str,
    report_id: str | None,
) -> None:
    content = render_template_html(
        cnv_path=cnv_input,
        annot_path=annotation_input,
        marcnv_path=marcnv_input,
        hybrid_path=hybrid_input,
        isv_path=isv_input,
        report_id=report_id,
    )

    output_path = os.path.abspath(output_html)
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with open(output_path, "w") as f:
        f.write(content)

    print(f"Report generated successfully at {output_path}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--id", type=str, help="Report ID")
    parser.add_argument("--annot", type=str, help="Path to the annotation file", required=True)
    parser.add_argument("--isv", type=str, help="Path to the ISV results", required=True)
    parser.add_argument("--marcnv", type=str, help="Path to the MarCNV results", required=True)
    parser.add_argument("--cnv", type=str, help="Path to the CNV region", required=True)
    parser.add_argument("--hybrid", type=str, help="Path to the hybrid results", required=True)
    parser.add_argument("--out_html", type=str, help="Path to the output HTML", required=True)

    args = parser.parse_args()
    genovisio_report(
        cnv_input=args.cnv,
        annotation_input=args.annot,
        isv_input=args.isv,
        marcnv_input=args.marcnv,
        output_html=args.out_html,
        hybrid_input=args.hybrid,
        report_id=args.id,
    )


if __name__ == "__main__":
    main()
