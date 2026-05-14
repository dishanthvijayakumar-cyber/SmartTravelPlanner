import random

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


# This file contains the complete machine-learning recommendation logic for the
# SmartTravel Streamlit app. The Results page passes the questionnaire answers
# into this file, and this file returns one ML Match Score from 0 to 100 for
# each destination.

# Codex was used as an assistant for creating this code/ python file

# A fixed random seed makes the generated training data and model training more
# reproducible. This is helpful for a university project because the team can
# explain and debug the model more easily.
RANDOM_SEED = 42

# This file name is used only if the team wants to save or load a trained model
# with joblib. The current Streamlit app can also train the model and cache it
# without uploading a .joblib file.
MODEL_FILE = "travel_match_model.joblib"

# The questionnaire uses labels like "Tropical" and "Temperate", while the ML
# model works with a smaller normalized climate vocabulary. This mapping keeps
# the feature engineering consistent.
CLIMATE_MAP = {
    "Cold": "cold",
    "Temperate": "mild",
    "Tropical": "warm",
    "Desert": "warm",
}

# scikit-learn models need numeric input. These dictionaries convert text
# categories into simple numeric codes.
CLIMATE_CODE = {"cold": 0, "mild": 1, "warm": 2}
BUDGET_CODE = {"low": 0, "medium": 1, "high": 2}

# These are the main travel-style categories from the questionnaire. Only the
# short label before the colon is used for ML matching.
TRAVEL_STYLES = [
    "Luxury Traveler",
    "Adventure Seeker",
    "Cultural Explorer",
    "Relaxation Focused",
    "Budget Backpacker",
]

# The model also needs travel styles as numbers, so each style receives a stable
# integer code based on its position in the list.
TRAVEL_STYLE_CODE = {style: index for index, style in enumerate(TRAVEL_STYLES)}

# These values match the travel pace selectbox used in the questionnaire.
TRAVEL_PACES = [
    "Relaxed: Take it slow, enjoy each moment",
    "Moderate: Balance of activities and rest",
    "Packed: See and do as much as possible",
]


def create_example_destinations():
    """
    Create fallback destination data for testing the ML file independently.

    The real app normally loads destinations from the existing project
    database. This fallback prevents the ML module from breaking if the database
    import is unavailable during development, presentation, or testing.
    """

    # The fallback data follows the same basic structure as the real database:
    # place, country, climate, budget range, description, and preference lists.
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
            "activities": [
                "Relaxation (Spas, Beach Days)",
                "Nature Hikes",
                "Adventure Activities (Ziplining, Rafting)",
            ],
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
            "activities": [
                "City Tours",
                "Historical Sites",
                "Cultural Experiences (Museums, Local Events)",
            ],
            "accommodation": ["Luxury Hotels", "Boutique Hotels"],
            "pace": ["Moderate: Balance of activities and rest"],
        },
    ]


def load_project_destinations():
    """
    Load destinations from the existing project database if available.

    If the database import fails, the function returns fallback destinations.
    This keeps the ML module usable even when it is tested outside the full
    Streamlit project.
    """

    try:
        # The project already contains a database module. Reusing it prevents
        # duplicate destination data and keeps the ML recommendations connected
        # to the same destinations shown elsewhere in the app.
        from database import get_destinations

        return get_destinations()
    except Exception:
        # A broad fallback is acceptable here because the app should still be
        # able to demonstrate the ML logic even if the database is unavailable.
        return create_example_destinations()


def get_text_before_colon(value):
    """
    Extract the short category label before a colon.

    Example: "Luxury Traveler: Premium Experiences" becomes "Luxury Traveler".
    This is needed because the questionnaire labels contain explanatory text,
    while the destination data stores only the shorter category names.
    """

    return str(value).split(":")[0].strip()


def ensure_list(value):
    """
    Convert values into list format for consistent matching.

    Streamlit multiselect answers are already lists, but database fields or
    fallback values can sometimes be None or a single string. This helper makes
    the overlap calculations safer.
    """

    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def budget_category_from_amount(amount):
    """
    Convert a numeric daily budget into a simple budget category.

    The model uses low / medium / high instead of raw amounts because category
    matches are easier to learn from the small example-style training dataset.
    """

    if amount <= 100:
        return "low"
    if amount <= 300:
        return "medium"
    return "high"


def budget_category_from_destination(destination):
    """
    Convert a destination budget range into low / medium / high.

    The destination contains a minimum and maximum expected budget. The average
    of that range is used as a simple representative budget level.
    """

    budget_min = destination.get("budget_min", 0)
    budget_max = destination.get("budget_max", budget_min)
    average_budget = (budget_min + budget_max) / 2
    return budget_category_from_amount(average_budget)


def normalize_climate(climate):
    """
    Convert questionnaire and database climate labels into model labels.

    Unknown climate values are converted to lowercase as a safe fallback.
    """

    return CLIMATE_MAP.get(climate, str(climate).lower())


def questionnaire_to_user_profile(preferences):
    """
    Convert Streamlit questionnaire answers into a compact ML user profile.

    The questionnaire stores user-friendly values in st.session_state. This
    function transforms those values into a consistent format that the feature
    engineering functions can use.
    """

    # Default values protect the app from missing session-state keys during
    # development or if a user reaches the Results page unexpectedly.
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
    Calculate how much two lists overlap.

    The result is between 0 and 1. A value of 1 means every selected user value
    appears in the destination values. A value of 0 means there is no overlap.
    """

    # Sets make the intersection calculation simple and avoid counting
    # duplicate values twice.
    user_set = set(ensure_list(user_values))
    destination_set = set(ensure_list(destination_values))

    # If the user did not select anything in a category, the app treats that
    # category as no match instead of dividing by zero.
    if not user_set:
        return 0

    return len(user_set.intersection(destination_set)) / len(user_set)


def calculate_criterion_scores(user, destination):
    """
    Calculate transparent 0-100 scores for each questionnaire criterion.

    These scores have two roles:
    1. They help create the rule-based target score for model training.
    2. They explain the final ML recommendation in charts on the Results page.
    """

    # Budget is scored first because the questionnaire budget is a numeric
    # slider, while each destination has a recommended budget range.
    budget_min = destination.get("budget_min", 0)
    budget_max = destination.get("budget_max", budget_min)
    daily_budget = user["daily_budget"]

    # A budget inside the destination range is a perfect fit. A matching budget
    # category is still useful, but less precise. Everything else gets a lower
    # score instead of zero so the model can still recommend diverse places.
    if budget_min <= daily_budget <= budget_max:
        budget_score = 100
    elif user["budget_category"] == budget_category_from_destination(destination):
        budget_score = 70
    else:
        budget_score = 35

    # Climate is a simple exact match after both values have been normalized.
    climate_score = 100 if user["climate"] == normalize_climate(destination.get("climate", "")) else 30

    # Travel style compares the user's selected style with the destination's
    # list of suitable travel styles.
    destination_styles = ensure_list(destination.get("styles", []))
    style_score = 100 if user["travel_style"] in destination_styles else 25

    # Interests and activities are multi-select fields, so they use an overlap
    # ratio rather than exact equality.
    interest_score = overlap_ratio(user["interests"], destination.get("interests", [])) * 100
    activity_score = overlap_ratio(user["activities"], destination.get("activities", [])) * 100

    # Accommodation is still kept in the ML logic for compatibility with the
    # questionnaire. The visual charts may hide it if the database does not
    # contain reliable accommodation information for all destinations.
    accommodation_score = overlap_ratio(user["accommodation"], destination.get("accommodation", [])) * 100

    # Travel pace is scored as a direct match against the destination's pace
    # categories.
    destination_paces = ensure_list(destination.get("pace", []))
    pace_score = 100 if user["travel_pace"] in destination_paces else 45

    # Rounding keeps the values readable in charts and tables.
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

    The RandomForestRegressor learns to approximate this rule-based score from
    numeric features. This approach is useful for a university prototype
    because there is no real historical user rating dataset yet.
    """

    criterion_scores = calculate_criterion_scores(user, destination)

    # The weights define how important each questionnaire category is for the
    # synthetic training label. They add up to 1.0, so the final score remains
    # on a 0-100 scale.
    weights = {
        "Budget": 0.18,
        "Climate": 0.14,
        "Style": 0.14,
        "Interests": 0.16,
        "Activities": 0.16,
        "Accommodation": 0.10,
        "Pace": 0.12,
    }

    # The final base score is a weighted average of all criterion scores.
    score = sum(criterion_scores[name] * weight for name, weight in weights.items())

    # The score is clipped to the expected user-facing range.
    return max(0, min(100, round(score, 1)))


def build_features(user, destination):
    """
    Convert one user-destination pair into numeric model features.

    This is the core feature engineering step. It turns text categories and
    list overlaps into numbers that RandomForestRegressor can process.
    """

    destination_budget = budget_category_from_destination(destination)
    destination_climate = normalize_climate(destination.get("climate", "Temperate"))
    criterion_scores = calculate_criterion_scores(user, destination)

    return {
        # Encoded category values tell the model which budget and climate group
        # the user and destination belong to.
        "user_budget_category": BUDGET_CODE[user["budget_category"]],
        "destination_budget_category": BUDGET_CODE[destination_budget],

        # Match flags are simple 0/1 features that make direct fits easy for
        # the model to detect.
        "budget_match": int(user["budget_category"] == destination_budget),
        "budget_fit_score": criterion_scores["Budget"],
        "user_climate": CLIMATE_CODE.get(user["climate"], 1),
        "destination_climate": CLIMATE_CODE.get(destination_climate, 1),
        "climate_match": int(user["climate"] == destination_climate),
        "user_style": TRAVEL_STYLE_CODE.get(user["travel_style"], 0),
        "style_match": int(user["travel_style"] in ensure_list(destination.get("styles", []))),

        # Overlap features preserve information from multi-select answers.
        "interest_overlap": criterion_scores["Interests"] / 100,
        "activity_overlap": criterion_scores["Activities"] / 100,
        "accommodation_overlap": criterion_scores["Accommodation"] / 100,
        "pace_match": int(user["travel_pace"] in ensure_list(destination.get("pace", []))),

        # Duration and destination budget range give the model additional
        # context beyond simple category matches.
        "travel_duration": user["travel_duration"],
        "destination_budget_min": destination.get("budget_min", 0),
        "destination_budget_max": destination.get("budget_max", 0),
    }


def create_random_user_profile():
    """
    Create one artificial user profile for model training.

    Because the project does not yet have real user rating data, the model is
    trained on many randomly generated questionnaire profiles.
    """

    # These pools mirror the options shown in the Streamlit questionnaire.
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

    # Random samples create variety in the synthetic training profiles. The
    # budget category is corrected later based on the random daily budget.
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


def create_training_data(destinations, number_of_users=150):
    """
    Generate training rows from random users and all destinations.

    For each artificial user, every destination becomes one training example.
    The label is the rule-based match score from calculate_base_match_score().
    """

    # Setting the seed here makes the generated artificial users reproducible.
    random.seed(RANDOM_SEED)
    rows = []

    for _ in range(number_of_users):
        user = create_random_user_profile()

        # The random profile chooses a daily budget first. This line derives the
        # correct low / medium / high category from that numeric amount.
        user["budget_category"] = budget_category_from_amount(user["daily_budget"])

        for destination in destinations:
            # Build numeric features and then add the target score that the
            # RandomForestRegressor should learn to predict.
            features = build_features(user, destination)
            features["target_score"] = calculate_base_match_score(user, destination)
            rows.append(features)

    return pd.DataFrame(rows)


def train_match_model(destinations=None):
    """
    Train the RandomForestRegressor and return the model with metadata.

    The returned model bundle contains:
    - the trained model
    - the exact feature column order
    - simple evaluation metrics for explanation and debugging
    """

    # If no destination list is provided, load the project destinations
    # automatically. This makes the function easy to call from Streamlit.
    if destinations is None:
        destinations = load_project_destinations()

    # Create synthetic training data based on random user profiles and all
    # available destinations.
    training_df = create_training_data(destinations)

    # X contains the input features. y contains the rule-based target score.
    X = training_df.drop(columns=["target_score"])
    y = training_df["target_score"]

    # A train/test split gives a simple way to evaluate how well the model
    # learned the synthetic scoring logic.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_SEED,
    )

    # RandomForestRegressor is used because it handles mixed numeric features
    # well and is understandable enough for a university prototype.
    model = RandomForestRegressor(
        n_estimators=40,
        random_state=RANDOM_SEED,
    )

    # Fit the model on the training part of the generated dataset.
    model.fit(X_train, y_train)

    # Evaluate predictions on the test split. These metrics are not shown to
    # every user, but they are useful for the team and teachers.
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
    Save the trained model bundle to disk with joblib.

    This is optional. It can be used if the team wants to train the model once
    offline and load it later instead of training it inside Streamlit.
    """

    # compress=3 keeps the file smaller while still being quick enough for a
    # small project model.
    joblib.dump(model_bundle, model_path, compress=3)


def load_saved_model(model_path=MODEL_FILE):
    """
    Load a previously saved model bundle from disk.

    This can be the fastest approach for deployment, but it requires the
    .joblib file to be available in the project environment.
    """

    return joblib.load(model_path)


def predict_destination_scores(questionnaire_preferences, destinations=None, model_bundle=None):
    """
    Predict ML Match Scores for all destinations and return a sorted DataFrame.

    This is the main function used by the Results page. It receives the user's
    questionnaire answers, builds features for each destination, predicts the
    ML Match Score, and returns the destinations from best to worst match.
    """

    # Load destinations if the caller did not provide them. In the app, the
    # Results page usually passes cached destinations for speed.
    if destinations is None:
        destinations = load_project_destinations()

    # Train a model if the caller did not provide one. In the app, this should
    # usually come from a cached train_model_cached() function.
    if model_bundle is None:
        model_bundle = train_match_model(destinations)

    # Convert the raw Streamlit questionnaire answers into the normalized user
    # profile used by the feature builder.
    user = questionnaire_to_user_profile(questionnaire_preferences)
    rows = []

    for destination in destinations:
        # Build exactly the same feature columns that were used during training.
        features = build_features(user, destination)
        features_df = pd.DataFrame([features], columns=model_bundle["feature_columns"])

        # Predict one score for this user-destination pair.
        predicted_score = model_bundle["model"].predict(features_df)[0]

        # Keep the displayed score inside the user-facing 0-100 range.
        predicted_score = max(0, min(100, predicted_score))

        # Criterion scores are added for explanation charts. They help users see
        # why a destination received a high or low score.
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

        # Add every criterion score as its own column, for example
        # "budget_score" or "climate_score". The chart file uses these columns.
        for criterion, score in criterion_scores.items():
            row[f"{criterion.lower()}_score"] = score

        rows.append(row)

    # Sort by the predicted ML Match Score so the best recommendations appear
    # first on the Results page.
    results_df = pd.DataFrame(rows)
    return results_df.sort_values(by="ml_match_score", ascending=False).reset_index(drop=True)
