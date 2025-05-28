# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from .prediction import load_data, preprocess

# Step 1: Load and preprocess data
df = load_data()

# Make sure the column 'Usage_Next_Month' exists in your CSV
if "Usage_Next_Month" not in df.columns:
    raise ValueError("Missing target column 'Usage_Next_Month' in the dataset.")

# Step 2: Feature encoding and selection
df_encoded, X, feature_cols = preprocess(df)

# Step 3: Set target variable
y = df["Usage_Next_Month"]  # Use the true next-month usage, not a predicted field

# Step 4: Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Step 5: Save the trained model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
joblib.dump(model, model_path)

print(f"✅ Model trained and saved to {model_path}")
