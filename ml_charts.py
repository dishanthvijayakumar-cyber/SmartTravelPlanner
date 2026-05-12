import plotly.graph_objects as go


# This file contains only chart-building functions for the ML results section.
# Keeping the visualizations in a separate file makes TravelPlannerResults.py
# easier to read and keeps the ML charts reusable.

# These columns are created by predict_destination_scores() in ml_travel_recommender.py.
# Each value represents how well one questionnaire area matches a destination.
CRITERIA_COLUMNS = [
    "budget_score",
    "climate_score",
    "style_score",
    "interests_score",
    "activities_score",
    "accommodation_score",
    "pace_score",
]

# Short labels for the chart axes. They are easier to read than the raw column names.
CRITERIA_LABELS = [
    "Budget",
    "Climate",
    "Style",
    "Interests",
    "Activities",
    "Accommodation",
    "Pace",
]

# Shared colors for a consistent SmartTravel look across all ML charts.
BACKGROUND = "#1a0030"
PAPER = "rgba(0,0,0,0)"
PURPLE = "#8a2be2"
LIGHT_PURPLE = "#c084fc"
ORANGE = "#f59e0b"
PINK = "#f472b6"
WHITE = "#ffffff"


def create_top3_radar_chart(ml_scores):
    """
    Create a radar chart that compares the Top-3 ML-ranked destinations.

    The chart uses the individual criterion scores instead of only the final
    ML match score. This helps users understand why a destination was ranked
    highly, for example because it fits budget, climate, or activities well.
    """

    # The DataFrame is already sorted by ML score before it reaches this chart.
    top_3 = ml_scores.head(3)
    fig = go.Figure()

    # Different colors and line styles make overlapping radar lines easier to see.
    colors = [ORANGE, LIGHT_PURPLE, PINK]
    dashes = ["solid", "dash", "dot"]

    for index, (_, row) in enumerate(top_3.iterrows()):
        # Read all criterion scores for one destination.
        values = [row[column] for column in CRITERIA_COLUMNS]

        # The first value is repeated at the end so the radar shape closes.
        closed_values = values + [values[0]]
        closed_labels = CRITERIA_LABELS + [CRITERIA_LABELS[0]]

        fig.add_trace(
            go.Scatterpolar(
                r=closed_values,
                theta=closed_labels,
                name=f"{row['destination']} ({row['ml_match_score']}/100)",
                mode="lines+markers",
                line=dict(color=colors[index], width=4, dash=dashes[index]),
                marker=dict(size=8, color=colors[index], line=dict(color=WHITE, width=1)),
                fill="toself",
                opacity=0.55,
            )
        )

    # The dark layout matches the existing Results page design.
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
    Create a heatmap for the Top-5 destinations and their criterion scores.

    This chart is useful because users can quickly compare which destination
    performs best for each individual questionnaire category.
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
            # Black text is intentionally used here so the score labels stay readable.
            textfont=dict(color="black", size=13),
            # Some older Plotly versions do not support "titlefont" directly on colorbar.
            # Keeping only "title" and "tickfont" avoids compatibility errors.
            colorbar=dict(title="Score", tickfont=dict(color=WHITE)),
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
    Show how the ML match score changes across the ranked destinations.

    If the line drops strongly, the first destination is clearly better than
    the rest. If it stays flat, several destinations are similarly suitable.
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
