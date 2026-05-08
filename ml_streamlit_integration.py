import matplotlib.pyplot as plt
import streamlit as st

from ml_travel_recommender import load_project_destinations, predict_destination_scores, train_match_model


# This file renders the ML-based recommendation section for TravelPlannerResults.py.
# It should be used on the Results page, not at the end of the questionnaire.

BACKGROUND = "#1a0030"
BAR_PURPLE = "#8a2be2"
LIGHT_PURPLE = "#c084fc"
ACCENT_ORANGE = "#f59e0b"
TEXT_WHITE = "#ffffff"
GRID_PURPLE = "#6a0dad"

CRITERIA = [
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


@st.cache_data
def load_destinations_cached():
    """Load project destinations once for Streamlit."""

    return load_project_destinations()


@st.cache_resource
def train_model_cached():
    """Train and cache the RandomForestRegressor once."""

    destinations = load_project_destinations()
    return train_match_model(destinations)


def style_axis(ax):
    """Apply the shared dark purple chart style."""

    ax.set_facecolor(BACKGROUND)
    ax.figure.set_facecolor(BACKGROUND)
    ax.tick_params(colors=TEXT_WHITE)
    ax.yaxis.label.set_color(TEXT_WHITE)
    ax.xaxis.label.set_color(TEXT_WHITE)
    ax.title.set_color(TEXT_WHITE)
    ax.grid(color=GRID_PURPLE, alpha=0.35)

    for spine in ax.spines.values():
        spine.set_color(BACKGROUND)


def create_ml_score_bar_chart(results_df):
    """Create a bar chart for the Top-10 ML Match Scores."""

    top_10 = results_df.head(10)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.bar(top_10["destination"], top_10["ml_match_score"], color=BAR_PURPLE)
    ax.set_ylabel("ML Match Score")
    ax.set_ylim(0, 100)
    ax.set_title("Top 10 Destinations by ML Match Score", pad=16)
    ax.tick_params(axis="x", rotation=-35)
    style_axis(ax)
    fig.tight_layout()

    return fig


def create_top3_radar_chart(results_df):
    """Create a radar chart comparing the criteria of the Top-3 destinations."""

    top_3 = results_df.head(3)
    angles = [index / float(len(CRITERIA)) * 2 * 3.14159 for index in range(len(CRITERIA))]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    colors = [BAR_PURPLE, ACCENT_ORANGE, LIGHT_PURPLE]

    for index, (_, row) in enumerate(top_3.iterrows()):
        values = [row[column] for column in CRITERIA]
        values += values[:1]
        ax.plot(angles, values, color=colors[index], linewidth=2, label=row["destination"])
        ax.fill(angles, values, color=colors[index], alpha=0.12)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(CRITERIA_LABELS, color=TEXT_WHITE)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], color=LIGHT_PURPLE)
    ax.grid(color=GRID_PURPLE, alpha=0.35)
    ax.set_title("Top 3 Criteria Comparison", color=TEXT_WHITE, pad=24)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), facecolor=BACKGROUND, labelcolor=TEXT_WHITE)

    return fig


def create_criteria_heatmap(results_df):
    """Create a heatmap showing criteria scores for the Top-5 destinations."""

    top_5 = results_df.head(5)
    heatmap_data = top_5[CRITERIA].to_numpy()

    fig, ax = plt.subplots(figsize=(10, 4.8))
    image = ax.imshow(heatmap_data, cmap="Purples", vmin=0, vmax=100)

    ax.set_xticks(range(len(CRITERIA_LABELS)))
    ax.set_xticklabels(CRITERIA_LABELS, rotation=35, ha="right", color=TEXT_WHITE)
    ax.set_yticks(range(len(top_5)))
    ax.set_yticklabels(top_5["destination"], color=TEXT_WHITE)
    ax.set_title("Criterion Strengths for Top 5 Destinations", pad=16)

    for row_index in range(len(top_5)):
        for column_index in range(len(CRITERIA)):
            value = heatmap_data[row_index, column_index]
            text_color = TEXT_WHITE if value < 65 else BACKGROUND
            ax.text(column_index, row_index, f"{value:.0f}", ha="center", va="center", color=text_color)

    colorbar = fig.colorbar(image, ax=ax)
    colorbar.ax.yaxis.set_tick_params(color=TEXT_WHITE)
    plt.setp(colorbar.ax.get_yticklabels(), color=TEXT_WHITE)

    style_axis(ax)
    fig.tight_layout()

    return fig


def create_score_distribution_chart(results_df):
    """Create a small line chart showing how ML scores fall across the ranking."""

    ranked = results_df.reset_index(drop=True).copy()
    ranked["rank"] = ranked.index + 1

    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.plot(ranked["rank"], ranked["ml_match_score"], marker="o", color=ACCENT_ORANGE, linewidth=2)
    ax.fill_between(ranked["rank"], ranked["ml_match_score"], color=ACCENT_ORANGE, alpha=0.18)
    ax.set_xlabel("Ranking Position")
    ax.set_ylabel("ML Match Score")
    ax.set_ylim(0, 100)
    ax.set_title("ML Score Drop Across All Ranked Destinations", pad=16)
    style_axis(ax)
    fig.tight_layout()

    return fig


def show_ml_results_page(preferences):
    """
    Render ML-based recommendations and graphics on the Results page.

    The Results page should pass st.session_state.preferences into this function.
    """

    destinations = load_destinations_cached()
    model_bundle = train_model_cached()
    results_df = predict_destination_scores(preferences, destinations, model_bundle)

    st.title("ML-Based Travel Recommendations")
    st.write("These destinations are ranked by a RandomForestRegressor using your questionnaire answers.")

    st.subheader("Top 10 Destinations")

    for rank, row in enumerate(results_df.head(10).itertuples(), start=1):
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(192,132,252,0.2);
                 border-radius:18px; padding:22px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap;">
                    <div>
                        <h3 style="margin:0; color:#ffffff;">#{rank} {row.destination}, {row.country}</h3>
                        <p style="color:#d8b4fe; margin:6px 0 0;">{row.description_sentence}</p>
                    </div>
                    <div style="text-align:center; min-width:120px;">
                        <div style="font-size:2rem; font-weight:900; color:#f59e0b;">{row.ml_match_score}</div>
                        <div style="font-size:0.8rem; color:#c084fc;">ML Match Score / 100</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("ML Match Score Chart")
    st.pyplot(create_ml_score_bar_chart(results_df))

    st.subheader("Top 3 Radar Chart")
    st.pyplot(create_top3_radar_chart(results_df))

    st.subheader("Criteria Heatmap")
    st.pyplot(create_criteria_heatmap(results_df))

    st.subheader("Score Distribution")
    st.pyplot(create_score_distribution_chart(results_df))

    with st.expander("Show ML score table"):
        display_columns = ["destination", "country", "ml_match_score"] + CRITERIA
        st.dataframe(results_df[display_columns], use_container_width=True)

    metrics = model_bundle["metrics"]
    st.caption(f"ML model: RandomForestRegressor | MAE: {metrics['mae']:.2f} | R2: {metrics['r2']:.2f}")
