"""API FastAPI que sirve el modelo entrenado (models/model.joblib)."""
import json
import logging
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("cancer-api")

MODEL_PATH = Path("models/model.joblib")
METRICS_PATH = Path("models/metrics.json")
CLASS_NAMES = {0: "maligno", 1: "benigno"}

app = FastAPI(
    title="Clasificador de tumores de mama (Breast Cancer Wisconsin)",
    description="Proyecto academico de Docker + ML. NO es una herramienta de diagnostico medico.",
    version="1.0.0",
)

model = joblib.load(MODEL_PATH)
metrics = json.loads(METRICS_PATH.read_text()) if METRICS_PATH.exists() else {}
FEATURES = list(metrics.get("features", []))
logger.info("Modelo cargado desde %s", MODEL_PATH)


class TumorFeatures(BaseModel):
    mean_radius: float = Field(..., gt=0)
    mean_texture: float = Field(..., gt=0)
    mean_perimeter: float = Field(..., gt=0)
    mean_area: float = Field(..., gt=0)
    mean_smoothness: float = Field(..., gt=0)
    mean_compactness: float = Field(..., ge=0)
    mean_concavity: float = Field(..., ge=0)
    mean_concave_points: float = Field(..., ge=0)
    mean_symmetry: float = Field(..., gt=0)
    mean_fractal_dimension: float = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "mean_radius": 13.03,
                "mean_texture": 18.42,
                "mean_perimeter": 82.61,
                "mean_area": 523.8,
                "mean_smoothness": 0.08983,
                "mean_compactness": 0.03766,
                "mean_concavity": 0.02562,
                "mean_concave_points": 0.02923,
                "mean_symmetry": 0.1467,
                "mean_fractal_dimension": 0.05863,
            }
        }
    }


@app.get("/")
def root():
    return {
        "message": "API de clasificacion de tumores de mama",
        "endpoints": {
            "GET /health": "Estado del servicio",
            "GET /model-info": "Metricas del modelo",
            "POST /predict": "Realiza una prediccion",
            "GET /docs": "Documentacion interactiva",
        },
    }


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.get("/model-info")
def model_info():
    return {"model": "StandardScaler + LogisticRegression", **metrics}


@app.post("/predict")
def predict(features: TumorFeatures):
    try:
        cols = FEATURES or list(TumorFeatures.model_fields.keys())
        data = features.model_dump()
        df = pd.DataFrame([[data[c] for c in cols]], columns=cols)
        pred = int(model.predict(df)[0])
        proba = model.predict_proba(df)[0]
        result = {
            "prediction": CLASS_NAMES[pred],
            "prediction_index": pred,
            "confidence": round(float(proba[pred]), 4),
            "probabilities": {CLASS_NAMES[i]: round(float(p), 4) for i, p in enumerate(proba)},
        }
        logger.info("Prediccion: %s (confianza %.4f)", result["prediction"], result["confidence"])
        return result
    except Exception as exc:
        logger.exception("Error durante la prediccion")
        raise HTTPException(status_code=500, detail=str(exc))
