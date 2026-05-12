import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# This file contains the visual UI helpers for the ML results section.
# It keeps charts and loading messages separate from TravelPlannerResults.py,
# so the main Results page stays easier to understand.

# These columns are produced by predict_destination_scores() in ml_travel_recommender.py.
# "accommodation_score" is intentionally not included because the current database
# does not contain reliable accommodation information for each destination.
CRITERIA_COLUMNS = [
    "budget_score",
    "climate_score",
    "style_score",
    "interests_score",
    "activities_score",
    "pace_score",
]

CRITERIA_LABELS = [
    "Budget",
    "Climate",
    "Style",
    "Interest",
    "Activity",
    "Pace",
]

# Shared colors keep all ML graphics visually consistent with the purple app design.
BACKGROUND = "#1a0030"
PAPER = "rgba(0,0,0,0)"
PURPLE = "#8a2be2"
LIGHT_PURPLE = "#c084fc"
ORANGE = "#f59e0b"
PINK = "#f472b6"
WHITE = "#ffffff"


def show_ml_loading_card(message="Calculating your personalized ML travel matches"):
    """
    Display a custom loading card while the ML model and scores are prepared.

    The function returns a Streamlit placeholder. After the ML calculation is
    finished, call loading_card.empty() to remove the loading message.
    """

    loading_card = st.empty()
    loading_card.markdown(
        f"""
        <style>
        .ml-loading-card {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(192,132,252,0.35);
            border-radius: 18px;
            padding: 18px 22px;
            margin: 16px 0 26px 0;
            box-shadow: 0 8px 28px rgba(0,0,0,0.22);
        }}
        .ml-loading-title {{
            color: #ffffff;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .ml-loading-text {{
            color: #d8b4fe;
            font-size: 0.9rem;
            margin-bottom: 12px;
        }}
        .ml-loading-bar {{
            height: 9px;
            overflow: hidden;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
        }}
        .ml-loading-bar::before {{
            content: "";
            display: block;
            width: 38%;
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #8a2be2, #c084fc, #f59e0b);
            animation: ml-slide 1.35s ease-in-out infinite;
        }}
        @keyframes ml-slide {{
            0% {{ transform: translateX(-110%); }}
            50% {{ transform: translateX(95%); }}
            100% {{ transform: translateX(280%); }}
        }}
        </style>

        <div class="ml-loading-card">
            <div class="ml-loading-title">{message}</div>
            <div class="ml-loading-text">
                The app is ranking destinations with the trained Random Forest model.
            </div>
            <div class="ml-loading-bar"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return loading_card


def create_ml_score_bar_chart(sorted_recommendations):
    """
    Create the main bar chart for the Top-10 ML-ranked destinations.

    The chart uses the ML match score already attached to each recommendation
    dictionary in TravelPlannerResults.py.
    """

    fig = go.Figure(
        data=[
            go.Bar(
                x=[destination["place"] for destination in sorted_recommendations],
                y=[destination["ml_match_score"] for destination in sorted_recommendations],
                marker=dict(color=PURPLE),
                hovertemplate="<b>%{x}</b><br>ML Match Score: %{y:.1f}/100<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Top 10 Destinations by ML Match Score",
        paper_bgcolor=PAPER,
        plot_bgcolor=BACKGROUND,
        font=dict(color=WHITE),
        xaxis=dict(title="", tickangle=-30, gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(title="ML Match Score", range=[0, 100], gridcolor="rgba(192,132,252,0.25)"),
        margin=dict(l=60, r=30, t=80, b=110),
        height=560,
    )

    return fig


def create_top3_separate_radar_charts(ml_scores):
    """
    Create three separate radar charts for the Top-3 ML destinations.

    Separate radar charts are easier to read than one combined radar chart
    because the destination lines no longer overlap each other.
    """

    top_3 = ml_scores.head(3)
    fig = make_subplots(
        rows=1,
        cols=3,
        horizontal_spacing=0.15,
        specs=[[{"type": "polar"}, {"type": "polar"}, {"type": "polar"}]],
        subplot_titles=[
            f"{row.destination}<br>{row.ml_match_score}/100"
            for row in top_3.itertuples()
        ],
    )

    colors = [ORANGE, LIGHT_PURPLE, PINK]

    for index, (_, row) in enumerate(top_3.iterrows(), start=1):
        values = [row[column] for column in CRITERIA_COLUMNS]

        # Repeat the first value at the end so the radar polygon closes.
        closed_values = values + [values[0]]
        closed_labels = CRITERIA_LABELS + [CRITERIA_LABELS[0]]

        fig.add_trace(
            go.Scatterpolar(
                r=closed_values,
                theta=closed_labels,
                mode="lines+markers",
                line=dict(color=colors[index - 1], width=4),
                marker=dict(size=8, color=colors[index - 1], line=dict(color=WHITE, width=1)),
                fill="toself",
                fillcolor=colors[index - 1],
                opacity=0.58,
                hovertemplate="%{theta}: %{r:.0f}/100<extra></extra>",
                showlegend=False,
            ),
            row=1,
            col=index,
        )

    # Apply the same polar-axis styling to all three subplots.
    polar_layout = dict(
        bgcolor=BACKGROUND,
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickfont=dict(color=LIGHT_PURPLE, size=10),
            gridcolor="rgba(192,132,252,0.35)",
        ),
        angularaxis=dict(
            tickfont=dict(color=WHITE, size=10),
            gridcolor="rgba(192,132,252,0.25)",
        ),
    )

    fig.update_layout(
        title="Top 3 ML Criteria Profiles",
        paper_bgcolor=PAPER,
        plot_bgcolor=BACKGROUND,
        font=dict(color=WHITE),
        polar=polar_layout,
        polar2=polar_layout,
        polar3=polar_layout,
        margin=dict(l=85, r=85, t=105, b=55),
        height=560,
    )

    return fig


def create_criteria_heatmap(ml_scores):
    """
    Create a heatmap for the Top-5 ML destinations.

    The heatmap shows which criteria helped each destination rank highly.
    Black text is used inside the cells to keep the numbers readable.
    """

    top_5 = ml_scores.head(5)
    z_values = top_5[CRITERIA_COLUMNS].to_numpy()

    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=CRITERIA_LABELS,
            y=top_5["destination"],
            colorscale=[
                [0.00, "#f8f4ff"],
                [0.35, "#d8b4fe"],
                [0.70, "#a855f7"],
                [1.00, "#f59e0b"],
            ],
            zmin=0,
            zmax=100,
            text=z_values,
            texttemplate="%{text:.0f}",
            textfont=dict(color="black", size=14),
            colorbar=dict(title="Score", tickfont=dict(color=WHITE)),
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:.1f}/100<extra></extra>",
        )
    )

    fig.update_layout(
        title="Top 5 ML Criterion Strengths",
        paper_bgcolor=PAPER,
        plot_bgcolor=BACKGROUND,
        font=dict(color=WHITE),
        xaxis=dict(tickangle=-20, gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(autorange="reversed", gridcolor="rgba(255,255,255,0.08)"),
        margin=dict(l=125, r=45, t=85, b=85),
        height=470,
    )

    return fig


def create_score_distribution_chart(ml_scores):
    """
    Show how the ML match score changes across the ranked destinations.

    This helps users see whether the first result is clearly ahead or whether
    several destinations are similarly strong matches.
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
            hovertemplate="Rank %{x}<br>ML Match Score: %{y:.1f}/100<extra></extra>",
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
