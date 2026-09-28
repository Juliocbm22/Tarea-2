"""Entrena el clasificador y guarda el modelo en models/model.joblib.

Uso:  python train.py
"""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_PATH = Path("data/breast_cancer.csv")
MODEL_PATH = Path("models/model.joblib")
METRICS_PATH = Path("models/metrics.json")

df = pd.read_csv(DATA_PATH)
X = df.drop(columns="diagnosis")
y = df["diagnosis"]
print(f"Dataset cargado: {X.shape[0]} muestras, {X.shape[1]} caracteristicas")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=7, stratify=y
)

# El Pipeline guarda escalador + modelo juntos en un solo archivo.
model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000)),
])
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy en prueba: {accuracy:.4f}\n")
print(classification_report(y_test, y_pred, target_names=["maligno", "benigno"]))

MODEL_PATH.parent.mkdir(exist_ok=True)
joblib.dump(model, MODEL_PATH)
METRICS_PATH.write_text(json.dumps({
    "accuracy": round(float(accuracy), 4),
    "n_train": int(len(X_train)),
    "n_test": int(len(X_test)),
    "features": list(X.columns),
}, indent=2))
print(f"Modelo guardado en {MODEL_PATH}")
