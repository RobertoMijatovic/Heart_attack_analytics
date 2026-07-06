import os
import json
import joblib
import pandas as pd
import tensorflow as tf

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
app = FastAPI(
    title="Heart Attack Analytics API",
    version="1.0"
)

app.mount(
    "/artifacts",
    StaticFiles(directory=ART_DIR),
    name="artifacts"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

rf_model = joblib.load(os.path.join(ART_DIR, "rf_model.joblib"))
preprocessor = joblib.load(os.path.join(ART_DIR, "preprocessor.joblib"))
dl_model = tf.keras.models.load_model(os.path.join(ART_DIR, "dl_model.keras"))

def load_json(filename):
    path = os.path.join(ART_DIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

kpis = load_json("kpis.json")
metrics = load_json("metrics.json")


class PredictRequest(BaseModel):
    age: int
    gender: str
    resting_bp: float
    cholesterol: float
    max_heart_rate: float
    bmi: float
    stress_level: float
    smoking_status: str
    diabetes: int
    family_history: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/kpis")
def get_kpis():
    return kpis

@app.get("/metrics")
def get_metrics():
    return metrics

@app.get("/plots")
def get_plots():
    files = [f for f in os.listdir(ART_DIR) if f.endswith(".png")]
    return {"plots": files}

@app.post("/predict")
def predict(req: PredictRequest):

    input_data = req.model_dump()

    full_input = {
        "age": input_data["age"],
        "gender": input_data["gender"],
        "chest_pain_type": "typical",
        "resting_bp": input_data["resting_bp"],
        "cholesterol": input_data["cholesterol"],
        "fasting_blood_sugar": 0,
        "resting_ecg": "normal",
        "max_heart_rate": input_data["max_heart_rate"],
        "exercise_angina": 0,
        "oldpeak": 1.0,
        "st_slope": "flat",
        "num_major_vessels": 0,
        "thalassemia": "normal",
        "bmi": input_data["bmi"],
        "smoking_status": input_data["smoking_status"],
        "alcohol_consumption": "low",
        "physical_activity": "medium",
        "family_history": input_data["family_history"],
        "diabetes": input_data["diabetes"],
        "stress_level": input_data["stress_level"]
    }

    df = pd.DataFrame([full_input])

    rf_pred = float(rf_model.predict(df)[0])

    X = preprocessor.transform(df)
    if hasattr(X, "toarray"):
        X = X.toarray()

    dl_pred = float(dl_model.predict(X, verbose=0)[0][0])

    rf_pred = max(0, min(1, rf_pred))
    dl_pred = max(0, min(1, dl_pred))

    final_score = (rf_pred + dl_pred) / 2

    if final_score < 0.33:
        risk = "Low Risk 🟢"
    elif final_score < 0.66:
        risk = "Medium Risk 🟡"
    else:
        risk = "High Risk 🔴"

    return {
        "rf_pred": rf_pred,
        "dl_pred": dl_pred,
        "final_score": final_score,
        "risk": risk
    }