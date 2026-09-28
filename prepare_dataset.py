"""Genera data/breast_cancer.csv a partir del dataset Breast Cancer Wisconsin
incluido en scikit-learn (no requiere internet).

Se usan solo las 10 caracteristicas "mean" para que la API sea manejable.
Etiqueta: diagnosis -> 0 = maligno, 1 = benigno.
"""
from pathlib import Path

from sklearn.datasets import load_breast_cancer

FEATURES = [
    "mean radius", "mean texture", "mean perimeter", "mean area",
    "mean smoothness", "mean compactness", "mean concavity",
    "mean concave points", "mean symmetry", "mean fractal dimension",
]

data = load_breast_cancer(as_frame=True)
df = data.frame[FEATURES + ["target"]].copy()
df.columns = [c.replace(" ", "_") for c in FEATURES] + ["diagnosis"]

Path("data").mkdir(exist_ok=True)
df.to_csv("data/breast_cancer.csv", index=False)
print(f"Dataset guardado en data/breast_cancer.csv -> {df.shape[0]} filas, {df.shape[1]} columnas")
print(df["diagnosis"].value_counts().rename({0: "maligno (0)", 1: "benigno (1)"}))
