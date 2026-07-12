import os
import json
from typing import Any

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import train


# =========================================================
# Putanje
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ART_DIR = os.path.join(BASE_DIR, "artifacts")
MODEL_DIR = os.path.join(BASE_DIR, "models")


# =========================================================
# FastAPI aplikacija
# =========================================================

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


# =========================================================
# Modeli
# =========================================================

rf_model: Any = None
preprocessor: Any = None
dl_model: Any = None


def load_models():
    global rf_model
    global preprocessor
    global dl_model

    rf_path = os.path.join(
        MODEL_DIR,
        "rf_model.joblib"
    )

    preprocessor_path = os.path.join(
        MODEL_DIR,
        "preprocessor.joblib"
    )

    dl_path = os.path.join(
        MODEL_DIR,
        "dl_model.keras"
    )

    if not os.path.exists(rf_path):
        raise FileNotFoundError(
            f"Random Forest model nije pronađen: {rf_path}"
        )

    if not os.path.exists(preprocessor_path):
        raise FileNotFoundError(
            f"Preprocessor nije pronađen: {preprocessor_path}"
        )

    if not os.path.exists(dl_path):
        raise FileNotFoundError(
            f"Deep Learning model nije pronađen: {dl_path}"
        )

    rf_model = joblib.load(rf_path)

    preprocessor = joblib.load(
        preprocessor_path
    )

    dl_model = tf.keras.models.load_model(
        dl_path
    )

    print("Modeli su učitani iz models foldera.")


load_models()


# =========================================================
# JSON podaci
# =========================================================

def load_json(filename):
    path = os.path.join(
        ART_DIR,
        filename
    )

    if not os.path.exists(path):
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


kpis = load_json("kpis.json")
metrics = load_json("metrics.json")


# =========================================================
# Model zahtjeva za predikciju
# =========================================================

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


# =========================================================
# Osnovne rute
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Heart Attack Analytics API",
        "documentation": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/kpis")
def get_kpis():
    return kpis


@app.get("/metrics")
def get_metrics():
    return metrics


@app.get("/plots")
def get_plots():
    files = sorted(
        filename
        for filename in os.listdir(ART_DIR)
        if filename.lower().endswith(".png")
    )

    return {
        "plots": files
    }


# =========================================================
# Ponovno treniranje
# =========================================================

@app.post("/retrain")
def retrain_models():
    global kpis
    global metrics

    try:
        result = train.main()

        # Učitavanje novostvorenih modela
        load_models()

        # Učitavanje novih statistika
        kpis = load_json("kpis.json")
        metrics = load_json("metrics.json")

        return {
            "status": "success",
            "message": (
                "Modeli, metrike, KPI pokazatelji "
                "i EDA grafovi uspješno su ažurirani."
            ),
            "result": result
        }

    except Exception as error:
        print(f"Retraining error: {error}")

        raise HTTPException(
            status_code=500,
            detail=(
                "Ponovno treniranje nije uspjelo: "
                f"{error}"
            )
        )


# =========================================================
# Predikcija
# =========================================================

@app.post("/predict")
def predict(req: PredictRequest):
    if (
        rf_model is None
        or preprocessor is None
        or dl_model is None
    ):
        raise HTTPException(
            status_code=503,
            detail="Modeli nisu učitani."
        )

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

    sample_df = pd.DataFrame(
        [full_input]
    )

    try:
        rf_pred = float(
            rf_model.predict_proba(
                sample_df
            )[0][1]
        )

        transformed_data = preprocessor.transform(
            sample_df
        )

        if hasattr(transformed_data, "toarray"):
            transformed_data = transformed_data.toarray()

        transformed_data = np.asarray(
            transformed_data,
            dtype=np.float32
        )

        dl_pred = float(
            dl_model.predict(
                transformed_data,
                verbose=0
            )[0][0]
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Predikcija nije uspjela: {error}"
        )

    rf_pred = float(
        np.clip(rf_pred, 0.0, 1.0)
    )

    dl_pred = float(
        np.clip(dl_pred, 0.0, 1.0)
    )

    final_score = (
        rf_pred + dl_pred
    ) / 2

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