import random

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


# This file contains the data and machine-learning logic for the travel match.
# It is intentionally simple for a university group project:
# 1. create example destination data
# 2. generate artificial training data
# 3. train a RandomForestRegressor
# 4. predict a 0-100 match score for each destination


# Scikit-learn needs numbers, so we convert text categories into numeric values.
BUDGET_MAP = {"low": 0, "medium": 1, "high": 2}
CLIMATE_MAP = {"cold": 0, "mild": 1, "warm": 2}
TRIP_LENGTH_MAP = {"short": 0, "medium": 1, "long": 2}

# These columns use values from 1 to 5 and represent travel preferences.
PREFERENCE_COLUMNS = ["beach", "culture", "nightlife", "nature", "adventure"]


def create_destinations_dataframe():
    """
    Create a small example dataset with travel destinations.

    In a larger real project, this data could come from a database or CSV file.
    For this project, keeping it inside a DataFrame makes the ML logic easy to
    understand and run locally.
    """

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
    """
    Store the user's questionnaire answers in the format required by the model.
    """

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
    Calculate a rule-based score from 0 to 100.

    This function creates the training labels for the RandomForestRegressor.
    The ML model learns to imitate these understandable matching rules.
    """

    score = 0

    # Exact matches for important categories receive fixed points.
    if user["budget"] == destination["budget"]:
        score += 15

    if user["climate"] == destination["climate"]:
        score += 15

    if user["trip_length"] == destination["trip_length"]:
        score += 10

    # For 1-5 preference values, smaller differences mean a better match.
    # Example: user beach=5 and destination beach=5 is better than beach=2.
    for column in PREFERENCE_COLUMNS:
        difference = abs(user[column] - destination[column])
        category_score = max(0, 12 - difference * 3)
        score += category_score

    # Make sure the score always stays within the required 0-100 range.
    return max(0, min(100, score))


def build_features(user, destination):
    """
    Convert one user-destination pair into numeric model features.

    We include raw encoded values and extra "fit" features. These fit features
    make the model easier to train because they directly describe how well the
    user and destination match.
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
    """
    Create a random user profile for artificial training data.

    Because we do not have real user ratings, we generate many possible users
    and score them with calculate_base_match_score().
    """

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
    Create training data from random user profiles and all destinations.

    Each row represents one possible user-destination combination.
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
    """
    Train the RandomForestRegressor and return the model plus evaluation metrics.
    """

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
    Predict and sort travel match scores for all destinations.

    Returns a DataFrame with the best destinations first.
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
