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
        df_encoded, _, feature_cols = preprocess(df)

        # Step 2: Load or train the model
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, "utils", "model.pkl")

        if not os.path.exists(model_path):
            print("🔄 Model not found. Training a new one...")
            from app.utils.train_model import train_model  # ✅ Import your training function
            train_model()  # ✅ Train and save model to model.pkl

        model = joblib.load(model_path)

        # Step 3: Generate predictions
        reorder_alerts = generate_reorder_alerts(df_encoded, model, feature_cols)

        return {"reorder_alerts": reorder_alerts}

    except Exception as e:
        print("".join(traceback.format_exception(None, e, e.__traceback__)))
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
