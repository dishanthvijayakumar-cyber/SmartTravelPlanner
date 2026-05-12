import plotly.graph_objects as go


# This file contains the ML result charts used on TravelPlannerResults.py.
# The charts use Plotly because it fits the existing Results page and keeps the
# visual style close to the current purple SmartTravel design.

CRITERIA_COLUMNS = [
    "budget_score",
    "climate_score",
    "style_score",
    "interests_score",
    "activities_score",
    "accommodation_score",
    "pace_score",
]

CRITERIA_LABELS = [
    "Budget",
    "Climate",
    "Style",
    "Interests",
    "Activities",
    "Accommodation",
    "Pace",
]

BACKGROUND = "#1a0030"
PAPER = "rgba(0,0,0,0)"
PURPLE = "#8a2be2"
LIGHT_PURPLE = "#c084fc"
ORANGE = "#f59e0b"
PINK = "#f472b6"
WHITE = "#ffffff"


def create_top3_radar_chart(ml_scores):
    """
    Create a radar chart for the Top-3 ML destinations.

    The line styles are intentionally different so that overlapping destinations
    are still readable: solid, dashed, dotted, with visible markers.
    """

    top_3 = ml_scores.head(3)
    fig = go.Figure()

    colors = [ORANGE, LIGHT_PURPLE, PINK]
    dashes = ["solid", "dash", "dot"]

    for index, (_, row) in enumerate(top_3.iterrows()):
        values = [row[column] for column in CRITERIA_COLUMNS]

        fig.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=CRITERIA_LABELS + [CRITERIA_LABELS[0]],
                name=f"{row['destination']} ({row['ml_match_score']}/100)",
                mode="lines+markers",
                line=dict(color=colors[index], width=4, dash=dashes[index]),
                marker=dict(size=8, color=colors[index], line=dict(color=WHITE, width=1)),
                fill="toself",
                opacity=0.55,
            )
        )

    fig.update_layout(
        title="Top 3 ML Criteria Comparison",
        paper_bgcolor=PAPER,
        plot_bgcolor=BACKGROUND,
        font=dict(color=WHITE),
        polar=dict(
            bgcolor=BACKGROUND,
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(192,132,252,0.35)",
                tickfont=dict(color=LIGHT_PURPLE),
            ),
            angularaxis=dict(
                gridcolor="rgba(192,132,252,0.25)",
                tickfont=dict(color=WHITE, size=12),
            ),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(color=WHITE),
        ),
        margin=dict(l=70, r=70, t=90, b=90),
        height=620,
    )

    return fig


def create_criteria_heatmap(ml_scores):
    """
    Create a heatmap for the Top-5 destinations and their ML criterion scores.

    The numbers are black for readability, as requested.
    """

    top_5 = ml_scores.head(5)
    z_values = top_5[CRITERIA_COLUMNS].to_numpy()

    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=CRITERIA_LABELS,
            y=top_5["destination"],
            colorscale=[
                [0.00, "#ede9fe"],
                [0.35, "#c084fc"],
                [0.70, "#8a2be2"],
                [1.00, "#f59e0b"],
            ],
            zmin=0,
            zmax=100,
            text=z_values,
            texttemplate="%{text:.0f}",
            textfont=dict(color="black", size=13),
            colorbar=dict(title="Score", tickfont=dict(color=WHITE), titlefont=dict(color=WHITE)),
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:.1f}/100<extra></extra>",
        )
    )

    fig.update_layout(
        title="Top 5 ML Criterion Strengths",
        paper_bgcolor=PAPER,
        plot_bgcolor=BACKGROUND,
        font=dict(color=WHITE),
        xaxis=dict(tickangle=-25, gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(autorange="reversed", gridcolor="rgba(255,255,255,0.08)"),
        margin=dict(l=120, r=40, t=80, b=90),
        height=460,
    )

    return fig


def create_score_distribution_chart(ml_scores):
    """
    Show how strongly the ML score drops across the ranked destinations.
    """

    ranked = ml_scores.reset_index(drop=True).copy()
    ranked["rank"] = ranked.index + 1

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ranked["rank"],
            y=ranked["ml_match_score"],
            mode="lines+markers",
            line=dict(color=ORANGE, width=4),
            marker=dict(size=8, color=ORANGE, line=dict(color=WHITE, width=1)),
            fill="tozeroy",
            fillcolor="rgba(245,158,11,0.18)",
            hovertemplate="Rank %{x}<br>ML Score: %{y:.1f}/100<extra></extra>",
        )
    )

    fig.update_layout(
        title="ML Score Distribution Across Ranked Destinations",
        paper_bgcolor=PAPER,
        plot_bgcolor=BACKGROUND,
        font=dict(color=WHITE),
        xaxis=dict(title="Ranking Position", gridcolor="rgba(192,132,252,0.25)"),
        yaxis=dict(title="ML Match Score", range=[0, 100], gridcolor="rgba(192,132,252,0.25)"),
        margin=dict(l=60, r=30, t=80, b=60),
        height=420,
    )

    return fig
