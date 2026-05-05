import random

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


# Category values are converted to numbers because scikit-learn models
# need numerical input features.
BUDGET_MAP = {"low": 0, "medium": 1, "high": 2}
CLIMATE_MAP = {"cold": 0, "mild": 1, "warm": 2}
TRIP_LENGTH_MAP = {"short": 0, "medium": 1, "long": 2}

# These are the 1-5 preference categories used by the questionnaire.
PREFERENCE_COLUMNS = ["beach", "culture", "nightlife", "nature", "adventure"]


def create_destinations_dataframe():
    """Create a small example dataset with travel destinations."""

    data = [
        ["Barcelona", "Spain", "medium", "warm", 5, 5, 4, 2, 3, "medium"],
        ["Reykjavik", "Iceland", "high", "cold", 1, 3, 2, 5, 5, "long"],
        ["Bali", "Indonesia", "medium", "warm", 5, 3, 3, 5, 4, "long"],
        ["Paris", "France", "high", "mild", 2, 5, 4, 2, 1, "medium"],
        ["Bangkok", "Thailand", "low", "warm", 3, 5, 5, 3, 3, "medium"],
        ["Cape Town", "South Africa", "medium", "warm", 4, 4, 3, 5, 5, "long"],
        ["Tokyo", "Japan", "high", "mild", 1, 5, 5, 2, 2, "long"],
        ["Lisbon", "Portugal", "medium", "warm", 4, 4, 4, 3, 2, "short"],
        ["Zurich", "Switzerland", "high", "cold", 1, 4, 2, 5, 3, "short"],
        ["Marrakech", "Morocco", "low", "warm", 1, 5, 3, 2, 4, "medium"],
        ["Vancouver", "Canada", "high", "mild", 2, 3, 3, 5, 4, "long"],
        ["Santorini", "Greece", "medium", "warm", 5, 4, 3, 2, 2, "short"],
    ]

    columns = [
        "destination",
        "country",
        "budget",
        "climate",
        "beach",
        "culture",
        "nightlife",
        "nature",
        "adventure",
        "trip_length",
    ]

    return pd.DataFrame(data, columns=columns)


def create_user_profile(
    budget,
    climate,
    beach,
    culture,
    nightlife,
    nature,
    adventure,
    trip_length,
):
    """Store the questionnaire answers in one simple dictionary."""

    return {
        "budget": budget,
        "climate": climate,
        "beach": beach,
        "culture": culture,
        "nightlife": nightlife,
        "nature": nature,
        "adventure": adventure,
        "trip_length": trip_length,
    }


def calculate_base_match_score(user, destination):
    """
    Calculate a simple rule-based score from 0 to 100.

    This score is used only to create training labels for the ML model.
    In a real product, these labels could later come from real user ratings.
    """

    score = 0

    # Exact matches for budget, climate, and trip length give fixed points.
    if user["budget"] == destination["budget"]:
        score += 15

    if user["climate"] == destination["climate"]:
        score += 15

    if user["trip_length"] == destination["trip_length"]:
        score += 10

    # For preference values, smaller differences are better.
    # Each category can contribute up to 12 points.
    for column in PREFERENCE_COLUMNS:
        difference = abs(user[column] - destination[column])
        category_score = max(0, 12 - difference * 3)
        score += category_score

    # Keep the result inside the 0-100 range.
    return max(0, min(100, score))


def build_features(user, destination):
    """
    Build numerical features for one user-destination combination.

    We use both raw encoded values and fit-features such as matches/differences.
    This makes the model easier to train and easier to explain.
    """

    features = {
        "user_budget": BUDGET_MAP[user["budget"]],
        "destination_budget": BUDGET_MAP[destination["budget"]],
        "budget_match": int(user["budget"] == destination["budget"]),
        "user_climate": CLIMATE_MAP[user["climate"]],
        "destination_climate": CLIMATE_MAP[destination["climate"]],
        "climate_match": int(user["climate"] == destination["climate"]),
        "user_trip_length": TRIP_LENGTH_MAP[user["trip_length"]],
        "destination_trip_length": TRIP_LENGTH_MAP[destination["trip_length"]],
        "trip_length_match": int(user["trip_length"] == destination["trip_length"]),
    }

    for column in PREFERENCE_COLUMNS:
        features[f"user_{column}"] = user[column]
        features[f"destination_{column}"] = destination[column]
        features[f"{column}_diff"] = abs(user[column] - destination[column])

    return features


def create_random_user_profile():
    """Create one random user profile for training data generation."""

    return {
        "budget": random.choice(list(BUDGET_MAP.keys())),
        "climate": random.choice(list(CLIMATE_MAP.keys())),
        "beach": random.randint(1, 5),
        "culture": random.randint(1, 5),
        "nightlife": random.randint(1, 5),
        "nature": random.randint(1, 5),
        "adventure": random.randint(1, 5),
        "trip_length": random.choice(list(TRIP_LENGTH_MAP.keys())),
    }


def create_training_data(destinations_df, number_of_users=500):
    """
    Create training rows from many random users and all destinations.

    Each row represents one user-destination combination.
    """

    rows = []

    for _ in range(number_of_users):
        user = create_random_user_profile()

        for _, destination in destinations_df.iterrows():
            features = build_features(user, destination)
            features["match_score"] = calculate_base_match_score(user, destination)
            rows.append(features)

    return pd.DataFrame(rows)


def train_match_model(destinations_df):
    """Train a RandomForestRegressor and return the model plus simple metrics."""

    training_df = create_training_data(destinations_df)

    X = training_df.drop(columns=["match_score"])
    y = training_df["match_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {
        "mae": mean_absolute_error(y_test, predictions),
        "r2": r2_score(y_test, predictions),
    }

    return model, metrics


def predict_destination_scores(user_profile, destinations_df, model):
    """
    Predict a match score for every destination and sort best matches first.
    """

    results = []

    for _, destination in destinations_df.iterrows():
        features = build_features(user_profile, destination)
        features_df = pd.DataFrame([features])

        predicted_score = model.predict(features_df)[0]
        predicted_score = max(0, min(100, predicted_score))

        results.append(
            {
                "destination": destination["destination"],
                "country": destination["country"],
                "predicted_score": round(predicted_score, 1),
                "budget": destination["budget"],
                "climate": destination["climate"],
                "trip_length": destination["trip_length"],
            }
        )

    results_df = pd.DataFrame(results)
    return results_df.sort_values(by="predicted_score", ascending=False)
