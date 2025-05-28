import traceback
from fastapi import APIRouter, HTTPException
from app.utils.prediction import load_data, preprocess, generate_reorder_alerts
import os
import joblib

router = APIRouter()

@router.get("/predict/reorder")
def predict_reorder():
    try:
        df = load_data()
        df_encoded, _, feature_cols = preprocess(df)

        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, "utils", "model.pkl")

        if not os.path.exists(model_path):
            raise HTTPException(status_code=500, detail="Prediction error: Model file not found.")

        model = joblib.load(model_path)

        reorder_alerts = generate_reorder_alerts(df_encoded, model, feature_cols)

        # Convert result to JSON
        return {"reorder_alerts": reorder_alerts.to_dict(orient="records")}

    except Exception as e:
        print("".join(traceback.format_exception(None, e, e.__traceback__)))  # Print full traceback in console
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
