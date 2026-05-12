from ml_travel_recommender import (
    MODEL_FILE,
    load_project_destinations,
    save_trained_model,
    train_match_model,
)


def main():
    """
    Train the ML model once and save it as a .joblib file.

    Run this script locally before starting the Streamlit app:
    python train_ml_model.py

    After it runs, upload travel_match_model.joblib to the GitHub repository.
    The Results page can then load the saved model instead of training live.
    """

    destinations = load_project_destinations()
    model_bundle = train_match_model(destinations)
    save_trained_model(model_bundle, MODEL_FILE)

    metrics = model_bundle["metrics"]
    print("ML model saved successfully.")
    print(f"Model file: {MODEL_FILE}")
    print(f"Destinations used: {len(destinations)}")
    print(f"MAE: {metrics['mae']:.2f}")
    print(f"R2: {metrics['r2']:.2f}")


if __name__ == "__main__":
    main()
