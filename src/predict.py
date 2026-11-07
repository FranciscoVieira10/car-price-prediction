
from pathlib import Path

import joblib
import pandas as pd


def load_model():
    project_root = Path(__file__).resolve().parent.parent
    model_path = project_root / "models" / "catboost_final.joblib"

    return joblib.load(model_path)


def predict_price(model, car):
    car_df = pd.DataFrame([car])

    if hasattr(model, "feature_names_"):
        car_df = car_df[model.feature_names_]

    predicted_price = model.predict(car_df)[0]

    return predicted_price
