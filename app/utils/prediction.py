#prediction.py
import pandas as pd
import joblib
import os


current_dir = os.path.dirname(__file__)  # Directory of prediction.py
csv_path = os.path.join(current_dir, 'extended_school_inventory_6_years.csv')
model_path = os.path.join(current_dir, 'model.pkl')

def load_data():
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    df['Month'] = pd.to_datetime(df['Month'], errors='coerce')
    df = df.dropna(subset=['Month'])
    df = df.sort_values(by='Month')
    df['Month_Num'] = df['Month'].dt.month
    df['Year'] = df['Month'].dt.year
    df['Prev_Quantity'] = df.groupby('Item Name')['Quantity Used'].shift(1)
    df = df.dropna()
    return df

def preprocess(df):
    df_encoded = pd.get_dummies(df, columns=["Category", "Item Name", "Condition"])
    feature_cols = ["Prev_Quantity", "Quantity Remaining", "Total Quantity"] + \
                   [col for col in df_encoded.columns if col.startswith("Category_") or 
                                                        col.startswith("Item Name_") or 
                                                        col.startswith("Condition_")]
    X = df_encoded[feature_cols]
    return df_encoded, X, feature_cols

def generate_reorder_alerts(df_encoded, model, feature_cols):
    df_encoded["Predicted_Usage"] = model.predict(df_encoded[feature_cols])
    df_encoded["Reorder_Alert"] = df_encoded["Predicted_Usage"] > df_encoded["Quantity Remaining"]
    reorder_items = df_encoded[df_encoded["Reorder_Alert"] == True]

    # Select relevant columns to return in the JSON
    columns_to_return = ["Category", "Item Name", "Quantity Remaining", "Predicted_Usage"]
    reorder_json = reorder_items[columns_to_return].to_dict(orient="records")

    return reorder_json


