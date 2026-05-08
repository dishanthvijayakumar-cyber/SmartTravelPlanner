import streamlit as st

from ml_travel_recommender import (
    create_destinations_dataframe,
    create_user_profile,
    predict_destination_scores,
    train_match_model,
)


# This file connects the existing Streamlit questionnaire with the ML model.
# Important: it does not create a second questionnaire. It reuses the answers
# the user already entered in TravelPlannerQuestionnaire.py.


@st.cache_data
def load_ml_destinations():
    """
    Load the example destination data once.

    Streamlit reruns the page often, so caching avoids unnecessary repeated work.
    """

    return create_destinations_dataframe()


@st.cache_resource
def load_ml_model():
    """
    Train the RandomForestRegressor once and cache the trained model.

    Without this cache, the model would train again after every button click or
    widget change, which would make the app feel slower.
    """

    destinations_df = create_destinations_dataframe()
    return train_match_model(destinations_df)


def convert_questionnaire_to_ml_profile(questionnaire_preferences):
    """
    Convert the existing questionnaire answers into the ML model format.

    The original questionnaire uses values such as:
    - daily budget as a number
    - climate as Tropical / Temperate / Cold / Desert
    - interests and activities as text lists

    The ML model expects simpler values:
    - budget: low / medium / high
    - climate: cold / mild / warm
    - beach, culture, nightlife, nature, adventure: values from 1 to 5
    - trip_length: short / medium / long
    """

    daily_budget = questionnaire_preferences.get("daily_budget", 50)
    ideal_climate = questionnaire_preferences.get("ideal_climate", "Temperate")
    interests = questionnaire_preferences.get("interests", [])
    activities = questionnaire_preferences.get("activities", [])
    travel_duration = questionnaire_preferences.get("travel_duration", 7)

    # Convert the numeric budget slider into the three budget categories.
    if daily_budget <= 100:
        budget = "low"
    elif daily_budget <= 300:
        budget = "medium"
    else:
        budget = "high"

    # Convert the questionnaire climate labels into the ML climate labels.
    climate_map = {
        "Cold": "cold",
        "Temperate": "mild",
        "Tropical": "warm",
        "Desert": "warm",
    }
    climate = climate_map.get(ideal_climate, "mild")

    # Convert travel duration in days into short / medium / long.
    if travel_duration <= 5:
        trip_length = "short"
    elif travel_duration <= 14:
        trip_length = "medium"
    else:
        trip_length = "long"

    # The original questionnaire has interests and activities as text answers.
    # We convert those text choices into simple 1-5 preference scores.
    combined_answers = interests + activities

    def score_from_keywords(keywords):
        """
        Return a 1-5 score based on whether selected answers contain keywords.

        This keeps the connection between the old questionnaire and the new ML
        model understandable for the presentation.
        """

        matches = 0
        for answer in combined_answers:
            for keyword in keywords:
                if keyword in answer:
                    matches += 1

        if matches >= 2:
            return 5
        if matches == 1:
            return 4
        return 2

    beach = score_from_keywords(["Beaches", "Beach", "Water Sports", "Relaxation"])
    culture = score_from_keywords(
        ["Culture", "Cultural", "History", "Historical", "Art", "Museums", "Architecture"]
    )
    nightlife = score_from_keywords(["Nightlife", "Bars", "Clubs"])
    nature = score_from_keywords(["Wildlife", "Mountains", "Hiking", "Nature", "Hikes"])
    adventure = score_from_keywords(["Adventure", "Ziplining", "Rafting", "Water Sports", "Hiking"])

    return create_user_profile(
        budget=budget,
        climate=climate,
        beach=beach,
        culture=culture,
        nightlife=nightlife,
        nature=nature,
        adventure=adventure,
        trip_length=trip_length,
    )


def show_ml_results_from_questionnaire(questionnaire_preferences):
    """
    Display ML recommendations based on the existing questionnaire answers.

    This function should be called at the end of TravelPlannerQuestionnaire.py.
    It shows only the ML result section, not another questionnaire.
    """

    destinations_df = load_ml_destinations()
    model, metrics = load_ml_model()
    user_profile = convert_questionnaire_to_ml_profile(questionnaire_preferences)

    st.header("ML Travel Match Score")
    st.write("Based on your questionnaire answers, these are your Top-3 ML recommendations.")

    if st.button("Calculate ML Top 3", key="ml_calculate_from_existing_questionnaire"):
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

        st.subheader("Top 3 Match Scores")
        chart_data = top_3.set_index("destination")["predicted_score"]
        st.bar_chart(chart_data)

        with st.expander("Show all ML scores"):
            st.dataframe(scores_df, use_container_width=True)

        st.caption(
            f"Model evaluation: MAE = {metrics['mae']:.2f}, R2 = {metrics['r2']:.2f}"
        )
