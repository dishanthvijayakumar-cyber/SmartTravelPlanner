import random

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


# This file contains the machine-learning recommendation logic.
# The Results page can call these functions after the existing questionnaire.
# The model then predicts one ML Match Score from 0 to 100 for every destination.


RANDOM_SEED = 42
MODEL_FILE = "travel_match_model.joblib"

CLIMATE_MAP = {
    "Cold": "cold",
    "Temperate": "mild",
    "Tropical": "warm",
    "Desert": "warm",
}

CLIMATE_CODE = {"cold": 0, "mild": 1, "warm": 2}
BUDGET_CODE = {"low": 0, "medium": 1, "high": 2}

TRAVEL_STYLES = [
    "Luxury Traveler",
    "Adventure Seeker",
    "Cultural Explorer",
    "Relaxation Focused",
    "Budget Backpacker",
]

TRAVEL_STYLE_CODE = {style: index for index, style in enumerate(TRAVEL_STYLES)}

TRAVEL_PACES = [
    "Relaxed: Take it slow, enjoy each moment",
    "Moderate: Balance of activities and rest",
    "Packed: See and do as much as possible",
]


def create_example_destinations():
    """
    Create fallback destination data.

    The real app already has a destination database. This fallback allows the
    ML file to still run in isolation for testing or presentation purposes.
    """

    return [
        {
            "place": "Singapore",
            "country": "Singapore",
            "climate": "Tropical",
            "budget_min": 180,
            "budget_max": 450,
            "description_sentence": "A clean, modern city with culture, food and nightlife.",
            "styles": ["Luxury Traveler", "Cultural Explorer"],
            "interests": ["Architecture", "Food & Cuisine", "Shopping", "Nightlife"],
            "activities": ["City Tours", "Shopping", "Nightlife (Bars, Clubs)"],
            "accommodation": ["Luxury Hotels", "Boutique Hotels"],
            "pace": ["Moderate: Balance of activities and rest"],
        },
        {
            "place": "Bali",
            "country": "Indonesia",
            "climate": "Tropical",
            "budget_min": 60,
            "budget_max": 220,
            "description_sentence": "A warm island destination with beaches, nature and relaxation.",
            "styles": ["Relaxation Focused", "Adventure Seeker"],
            "interests": ["Beaches", "Wildlife", "Food & Cuisine"],
            "activities": ["Relaxation (Spas, Beach Days)", "Nature Hikes", "Adventure Activities (Ziplining, Rafting)"],
            "accommodation": ["Resorts", "Vacation Rentals (Airbnb, etc.)"],
            "pace": ["Relaxed: Take it slow, enjoy each moment"],
        },
        {
            "place": "Paris",
            "country": "France",
            "climate": "Temperate",
            "budget_min": 160,
            "budget_max": 500,
            "description_sentence": "A cultural capital known for museums, architecture and cuisine.",
            "styles": ["Luxury Traveler", "Cultural Explorer"],
            "interests": ["Architecture", "History", "Art & Museums", "Food & Cuisine"],
            "activities": ["City Tours", "Historical Sites", "Cultural Experiences (Museums, Local Events)"],
            "accommodation": ["Luxury Hotels", "Boutique Hotels"],
            "pace": ["Moderate: Balance of activities and rest"],
        },
    ]


def load_project_destinations():
    """
    Load destinations from the existing project database if available.

    If the project database cannot be imported, fallback example data is used.
    """

    try:
        from database import get_destinations

        return get_destinations()
    except Exception:
        return create_example_destinations()


def get_text_before_colon(value):
    """
    Convert labels like 'Luxury Traveler: Premium Experiences' to 'Luxury Traveler'.
    """

    return str(value).split(":")[0].strip()


def ensure_list(value):
    """
    Convert missing values to an empty list and single strings to a one-item list.
    """

    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def budget_category_from_amount(amount):
    """
    Convert the questionnaire budget slider into low / medium / high.
    """

    if amount <= 100:
        return "low"
    if amount <= 300:
        return "medium"
    return "high"


def budget_category_from_destination(destination):
    """
    Convert destination budget range into low / medium / high.
    """

    budget_min = destination.get("budget_min", 0)
    budget_max = destination.get("budget_max", budget_min)
    average_budget = (budget_min + budget_max) / 2
    return budget_category_from_amount(average_budget)


def normalize_climate(climate):
    """
    Convert questionnaire/database climate labels into model climate labels.
    """

    return CLIMATE_MAP.get(climate, str(climate).lower())


def questionnaire_to_user_profile(preferences):
    """
    Convert the existing questionnaire answers into a compact ML user profile.
    """

    daily_budget = preferences.get("daily_budget", 50)
    travel_duration = preferences.get("travel_duration", 7)

    return {
        "travel_style": get_text_before_colon(preferences.get("travel_style", TRAVEL_STYLES[0])),
        "climate": normalize_climate(preferences.get("ideal_climate", "Temperate")),
        "daily_budget": daily_budget,
        "budget_category": budget_category_from_amount(daily_budget),
        "interests": ensure_list(preferences.get("interests", [])),
        "activities": ensure_list(preferences.get("activities", [])),
        "accommodation": ensure_list(preferences.get("accommodation", [])),
        "travel_pace": preferences.get("travel_pace", TRAVEL_PACES[1]),
        "travel_duration": travel_duration,
    }


def overlap_ratio(user_values, destination_values):
    """
    Calculate how much two text lists overlap.

    The result is between 0 and 1.
    """

    user_set = set(ensure_list(user_values))
    destination_set = set(ensure_list(destination_values))

    if not user_set:
        return 0

    return len(user_set.intersection(destination_set)) / len(user_set)


def calculate_criterion_scores(user, destination):
    """
    Calculate understandable 0-100 criterion scores.

    These criterion scores are used both for training labels and for charts.
    """

    budget_min = destination.get("budget_min", 0)
    budget_max = destination.get("budget_max", budget_min)
    daily_budget = user["daily_budget"]

    if budget_min <= daily_budget <= budget_max:
        budget_score = 100
    elif user["budget_category"] == budget_category_from_destination(destination):
        budget_score = 70
    else:
        budget_score = 35

    climate_score = 100 if user["climate"] == normalize_climate(destination.get("climate", "")) else 30

    destination_styles = ensure_list(destination.get("styles", []))
    style_score = 100 if user["travel_style"] in destination_styles else 25

    interest_score = overlap_ratio(user["interests"], destination.get("interests", [])) * 100
    activity_score = overlap_ratio(user["activities"], destination.get("activities", [])) * 100
    accommodation_score = overlap_ratio(user["accommodation"], destination.get("accommodation", [])) * 100

    destination_paces = ensure_list(destination.get("pace", []))
    pace_score = 100 if user["travel_pace"] in destination_paces else 45

    return {
        "Budget": round(budget_score, 1),
        "Climate": round(climate_score, 1),
        "Style": round(style_score, 1),
        "Interests": round(interest_score, 1),
        "Activities": round(activity_score, 1),
        "Accommodation": round(accommodation_score, 1),
        "Pace": round(pace_score, 1),
    }


def calculate_base_match_score(user, destination):
    """
    Create a transparent rule-based score used as the ML training target.

    The RandomForestRegressor learns to approximate this score from features.
    """

    criterion_scores = calculate_criterion_scores(user, destination)

    weights = {
        "Budget": 0.18,
        "Climate": 0.14,
        "Style": 0.14,
        "Interests": 0.16,
        "Activities": 0.16,
        "Accommodation": 0.10,
        "Pace": 0.12,
    }

    score = sum(criterion_scores[name] * weight for name, weight in weights.items())
    return max(0, min(100, round(score, 1)))


def build_features(user, destination):
    """
    Convert one user-destination pair into numeric ML features.
    """

    destination_budget = budget_category_from_destination(destination)
    destination_climate = normalize_climate(destination.get("climate", "Temperate"))
    criterion_scores = calculate_criterion_scores(user, destination)

    return {
        "user_budget_category": BUDGET_CODE[user["budget_category"]],
        "destination_budget_category": BUDGET_CODE[destination_budget],
        "budget_match": int(user["budget_category"] == destination_budget),
        "budget_fit_score": criterion_scores["Budget"],
        "user_climate": CLIMATE_CODE.get(user["climate"], 1),
        "destination_climate": CLIMATE_CODE.get(destination_climate, 1),
        "climate_match": int(user["climate"] == destination_climate),
        "user_style": TRAVEL_STYLE_CODE.get(user["travel_style"], 0),
        "style_match": int(user["travel_style"] in ensure_list(destination.get("styles", []))),
        "interest_overlap": criterion_scores["Interests"] / 100,
        "activity_overlap": criterion_scores["Activities"] / 100,
        "accommodation_overlap": criterion_scores["Accommodation"] / 100,
        "pace_match": int(user["travel_pace"] in ensure_list(destination.get("pace", []))),
        "travel_duration": user["travel_duration"],
        "destination_budget_min": destination.get("budget_min", 0),
        "destination_budget_max": destination.get("budget_max", 0),
    }


def create_random_user_profile():
    """
    Create one artificial user profile for model training.
    """

    interests_pool = [
        "Photography",
        "Food & Cuisine",
        "Wildlife",
        "Architecture",
        "Beaches",
        "Mountains",
        "History",
        "Nightlife",
        "Shopping",
        "Art & Museums",
        "Hiking",
        "Water Sports",
    ]

    activities_pool = [
        "City Tours",
        "Nature Hikes",
        "Cultural Experiences (Museums, Local Events)",
        "Adventure Activities (Ziplining, Rafting)",
        "Relaxation (Spas, Beach Days)",
        "Food & Drink Experiences (Cooking Classes, Wine Tasting)",
        "Nightlife (Bars, Clubs)",
        "Shopping",
        "Wildlife Encounters",
        "Historical Sites",
    ]

    accommodation_pool = [
        "Luxury Hotels",
        "Mid-range Hotels",
        "Budget Hotels",
        "Cabins",
        "Camping",
        "Hostels",
        "Vacation Rentals (Airbnb, etc.)",
        "Boutique Hotels",
        "Resorts",
        "Bed & Breakfasts",
    ]

    return {
        "travel_style": random.choice(TRAVEL_STYLES),
        "climate": random.choice(list(CLIMATE_CODE.keys())),
        "daily_budget": random.randint(20, 600),
        "budget_category": "medium",
        "interests": random.sample(interests_pool, random.randint(1, 4)),
        "activities": random.sample(activities_pool, random.randint(1, 4)),
        "accommodation": random.sample(accommodation_pool, random.randint(1, 3)),
        "travel_pace": random.choice(TRAVEL_PACES),
        "travel_duration": random.choice([3, 5, 7, 10, 14, 21, 30]),
    }


def create_training_data(destinations, number_of_users=700):
    """
    Generate training rows from random users and all destinations.
    """

    random.seed(RANDOM_SEED)
    rows = []

    for _ in range(number_of_users):
        user = create_random_user_profile()
        user["budget_category"] = budget_category_from_amount(user["daily_budget"])

        for destination in destinations:
            features = build_features(user, destination)
            features["target_score"] = calculate_base_match_score(user, destination)
            rows.append(features)

    return pd.DataFrame(rows)


def train_match_model(destinations=None):
    """
    Train the RandomForestRegressor and return the model with evaluation metrics.
    """

    if destinations is None:
        destinations = load_project_destinations()

    training_df = create_training_data(destinations)

    X = training_df.drop(columns=["target_score"])
    y = training_df["target_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_SEED,
    )

    model = RandomForestRegressor(
        n_estimators=120,
        random_state=RANDOM_SEED,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    metrics = {
        "mae": mean_absolute_error(y_test, predictions),
        "r2": r2_score(y_test, predictions),
    }

    return {
        "model": model,
        "feature_columns": list(X.columns),
        "metrics": metrics,
    }


def save_trained_model(model_bundle, model_path=MODEL_FILE):
    """
    Save the trained RandomForestRegressor bundle to disk.

    The bundle contains:
    - the trained model
    - the feature column order
    - simple evaluation metrics
    """

    joblib.dump(model_bundle, model_path)


def load_saved_model(model_path=MODEL_FILE):
    """
    Load a pre-trained model from disk.

    This is the fast path for the Streamlit Results page. Instead of training
    the RandomForestRegressor while the user waits, the app only loads the
    already trained model file and immediately predicts scores.
    """

    return joblib.load(model_path)


def predict_destination_scores(questionnaire_preferences, destinations=None, model_bundle=None):
    """
    Predict ML Match Scores for all destinations and sort by highest score.
    """

    if destinations is None:
        destinations = load_project_destinations()

    if model_bundle is None:
        model_bundle = train_match_model(destinations)

    user = questionnaire_to_user_profile(questionnaire_preferences)
    rows = []

    for destination in destinations:
        features = build_features(user, destination)
        features_df = pd.DataFrame([features], columns=model_bundle["feature_columns"])
        predicted_score = model_bundle["model"].predict(features_df)[0]
        predicted_score = max(0, min(100, predicted_score))
        criterion_scores = calculate_criterion_scores(user, destination)

        row = {
            "destination": destination.get("place", destination.get("destination", "Unknown")),
            "country": destination.get("country", ""),
            "description_sentence": destination.get("description_sentence", ""),
            "ml_match_score": round(predicted_score, 1),
            "budget_min": destination.get("budget_min", 0),
            "budget_max": destination.get("budget_max", 0),
            "climate": destination.get("climate", ""),
        }

        for criterion, score in criterion_scores.items():
            row[f"{criterion.lower()}_score"] = score

        rows.append(row)

    results_df = pd.DataFrame(rows)
    return results_df.sort_values(by="ml_match_score", ascending=False).reset_index(drop=True)
