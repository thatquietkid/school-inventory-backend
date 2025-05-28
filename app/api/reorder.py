import traceback
from fastapi import APIRouter, HTTPException
from app.utils.prediction import load_data, preprocess, generate_reorder_alerts
import os
import joblib

router = APIRouter()

@router.get("/predict/reorder")
def predict_reorder():
    try:
        # Step 1: Load and preprocess the data
        df = load_data()
        df_encoded, X, feature_cols = preprocess(df)

        # Step 2: Load the trained model
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, "utils", "model.pkl")

        if not os.path.exists(model_path):
            raise HTTPException(status_code=500, detail="Prediction error: Model file not found.")

        model = joblib.load(model_path)

        # Step 3: Predict only usage
        y_pred = model.predict(X)
        df["Expected_Usage"] = y_pred

        # Step 4: Derive recommendations
        df["Recommended_Procurement"] = df["Expected_Usage"] * 1.10
        df["Waste_Risk"] = df["Procurement_Last_Month"] > df["Expected_Usage"] * 1.2
        df["Stockout_Risk"] = df["Procurement_Last_Month"] < df["Expected_Usage"] * 0.8

        # Step 5: Select useful columns to return
        result = df[[
            "Category",
            "Item Name",
            "Expected_Usage",
            "Recommended_Procurement",
            "Procurement_Last_Month",
            "Waste_Risk",
            "Stockout_Risk"
        ]]

        return {"reorder_analysis": result.to_dict(orient="records")}

    except Exception as e:
        print("".join(traceback.format_exception(None, e, e.__traceback__)))
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
