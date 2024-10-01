from typing import Any

import plotly.graph_objects as go


def get_base_trace() -> dict[str, Any]:
    return {
        "text": ["B", "LB", "VUS", "LP", "P", " "],
        "marker": {
            "colors": [
                "rgba(154, 205, 50, 0.3)",
                "rgba(144, 238, 144, 0.3)",
                "rgba(255, 255, 0, 0.3)",
                "rgba(255, 165, 0, 0.3)",
                "rgba(255, 0, 0, 0.3)",
                "white",
            ],
            "line": {
                "color": [
                    "rgba(154, 205, 50, 1)",
                    "rgba(144, 238, 144, 1)",
                    "rgba(255, 230, 0, 1)",
                    "rgba(255, 165, 0, 1)",
                    "rgba(255, 0, 0, 1)",
                    "white",
                ],
                "width": [0, 0, 0, 0, 0, 0],
            },
        },
        "pull": [0, 0, 0, 0, 0, 0],
    }


def emphasize_trace(trace: dict[str, Any], index: int) -> dict[str, Any]:
    trace["pull"][index] = 0.1
    trace["text"][index] = "<b>{val}</b>".format(val=trace["text"][index])
    trace["marker"]["line"]["width"][index] = 3
    if index == 0:
        trace["marker"]["colors"][0] = "rgba(154, 205, 50, 0.6)"
        # trace['marker']['line']['color'][0] = "rgba(154, 205, 50, 1)"
    elif index == 1:
        trace["marker"]["colors"][1] = "rgba(144, 238, 144, 0.6)"
        # trace['marker']['line']['color'][1] = "rgba(144, 238, 144, 1)"
    elif index == 2:
        trace["marker"]["colors"][2] = "rgba(255, 230, 0, 0.6)"
        # trace['marker']['line']['color'][2] = "rgba(255, 230, 0, 1)"
    elif index == 3:
        trace["marker"]["colors"][3] = "rgba(255, 165, 0, 0.6)"
        # trace['marker']['line']['color'][3] = "rgba(255, 165, 0, 1)"
    else:
        trace["marker"]["colors"][4] = "rgba(255, 0, 0, 0.6)"
        # trace['marker']['line']['color'][4] = "rgba(255, 0, 0, 1)"
    return trace


def set_color(trace: dict[str, Any], score: float, type: str) -> dict[str, Any]:
    # TODO this should not be inferred from classification severity level?
    if type == "marcnv":
        if score <= -0.9:
            trace = emphasize_trace(trace, 0)
        elif score > -0.9 and score < -0.5:
            trace = emphasize_trace(trace, 1)
        elif score >= -0.5 and score <= 0.5:
            trace = emphasize_trace(trace, 2)
        elif score > 0.5 and score < 0.9:
            trace = emphasize_trace(trace, 3)
        else:
            trace = emphasize_trace(trace, 4)
    elif type == "isv":
        if score <= 0.1:
            trace = emphasize_trace(trace, 0)
        elif score > 0.1 and score < 0.25:
            trace = emphasize_trace(trace, 1)
        elif score >= 0.25 and score <= 0.75:
            trace = emphasize_trace(trace, 2)
        elif score > 0.75 and score < 0.9:
            trace = emphasize_trace(trace, 3)
        else:
            trace = emphasize_trace(trace, 4)
    elif type == "hybrid":
        if score <= 0.2:
            trace = emphasize_trace(trace, 0)
        elif score > 0.2 and score < 0.4:
            trace = emphasize_trace(trace, 1)
        elif score >= 0.4 and score <= 0.6:
            trace = emphasize_trace(trace, 2)
        elif score > 0.6 and score < 0.8:
            trace = emphasize_trace(trace, 3)
        else:
            trace = emphasize_trace(trace, 4)
    return trace


def create_prediction_plot(score: float, type: str) -> str:
    trace = get_base_trace()
    trace = set_color(trace, score, type)
    fig = go.Figure()
    fig.add_pie(
        values=[100 / 5, 100 / 5, 100 / 5, 100 / 5, 100 / 5, 100],
        hole=0.4,
        rotation=90,
        marker=trace["marker"],
        pull=trace["pull"],
        text=trace["text"],
        direction="clockwise",
        textinfo="text",
        textposition="inside",
        hoverinfo="label",
        labels=["B", "LB", "VUS", "LP", "P", " "],
        showlegend=False,
    )
    fig.update_layout(template="plotly_white", height=150, width=150, margin=dict(l=1, r=1, t=1, b=1))
    fig.update_xaxes(visible=False, range=[-1, 1])
    fig.update_yaxes(visible=False, range=[-1, 1])
    return fig.to_json()
