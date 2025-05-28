# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from .prediction import load_data, preprocess

# Load and preprocess data
df = load_data()
df_encoded, X, feature_cols = preprocess(df)

# Target variable
y = df_encoded["Predicted_Usage"]

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
joblib.dump(model, model_path)

print(f"Model trained and saved to {model_path}")
