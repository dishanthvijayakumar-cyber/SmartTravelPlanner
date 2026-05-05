import streamlit as st

from ml_travel_recommender import (
    create_destinations_dataframe,
    create_user_profile,
    predict_destination_scores,
    train_match_model,
)


@st.cache_data
def load_ml_destinations():
    """Load the example destinations once for the Streamlit app."""

    return create_destinations_dataframe()


@st.cache_resource
def load_ml_model():
    """
    Train the RandomForest model once and cache it.

    Streamlit reruns the script after interactions. Without caching, the model
    would be trained again after every click or slider change.
    """

    destinations_df = create_destinations_dataframe()
    return train_match_model(destinations_df)


def show_ml_travel_match_section():
    """
    Show the complete ML travel match section inside an existing Streamlit page.

    Import this function in TravelPlannerDemo.py or at the end of your
    questionnaire file, then call show_ml_travel_match_section().
    """

    destinations_df = load_ml_destinations()
    model, metrics = load_ml_model()

    st.header("Personalized Travel Match Score")
    st.write("Answer the questions and get your Top-3 travel recommendations.")

    budget = st.selectbox(
        "Budget",
        ["low", "medium", "high"],
        key="ml_budget",
    )

    climate = st.selectbox(
        "Preferred climate",
        ["cold", "mild", "warm"],
        key="ml_climate",
    )

    beach = st.slider("Beach", 1, 5, 3, key="ml_beach")
    culture = st.slider("Culture", 1, 5, 3, key="ml_culture")
    nightlife = st.slider("Nightlife", 1, 5, 3, key="ml_nightlife")
    nature = st.slider("Nature", 1, 5, 3, key="ml_nature")
    adventure = st.slider("Adventure", 1, 5, 3, key="ml_adventure")

    trip_length = st.selectbox(
        "Trip length",
        ["short", "medium", "long"],
        key="ml_trip_length",
    )

    if st.button("Calculate Travel Match", key="ml_calculate_match"):
        user_profile = create_user_profile(
            budget=budget,
            climate=climate,
            beach=beach,
            culture=culture,
            nightlife=nightlife,
            nature=nature,
            adventure=adventure,
            trip_length=trip_length,
        )

        scores_df = predict_destination_scores(
            user_profile=user_profile,
            destinations_df=destinations_df,
            model=model,
        )

        top_3 = scores_df.head(3)

        st.subheader("Top 3 Recommendations")

        for rank, row in enumerate(top_3.itertuples(), start=1):
            st.markdown(
                f"""
                **#{rank} {row.destination}, {row.country}**  
                Match Score: **{row.predicted_score}/100**  
                Budget: `{row.budget}` | Climate: `{row.climate}` | Trip length: `{row.trip_length}`
                """
            )

        st.subheader("Best Destination Scores")
        chart_data = top_3.set_index("destination")["predicted_score"]
        st.bar_chart(chart_data)

        with st.expander("Show all destination scores"):
            st.dataframe(scores_df, use_container_width=True)

        st.caption(
            f"Model evaluation: MAE = {metrics['mae']:.2f}, R2 = {metrics['r2']:.2f}"
        )
