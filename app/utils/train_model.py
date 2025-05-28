# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from .prediction import load_data, preprocess

def train_model():
    df = load_data()
    df_encoded, X, feature_cols = preprocess(df)

    if "Usage_Next_Month" not in df.columns:
        raise ValueError("Missing target column 'Usage_Next_Month' in the dataset.")

    y = df["Usage_Next_Month"]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    joblib.dump(model, model_path)

    print(f"✅ Model trained and saved to {model_path}")
