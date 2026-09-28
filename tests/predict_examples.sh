#!/usr/bin/env bash
# Envia dos predicciones de ejemplo a la API (ajusta el puerto si usas 8001)
URL="${1:-http://localhost:8000}"

echo "== Health =="
curl -s "$URL/health"; echo; echo

echo "== Ejemplo BENIGNO =="
curl -s -X POST "$URL/predict" -H "Content-Type: application/json" -d '{
  "mean_radius": 13.03, "mean_texture": 18.42, "mean_perimeter": 82.61,
  "mean_area": 523.8, "mean_smoothness": 0.08983, "mean_compactness": 0.03766,
  "mean_concavity": 0.02562, "mean_concave_points": 0.02923,
  "mean_symmetry": 0.1467, "mean_fractal_dimension": 0.05863 }'
echo; echo

echo "== Ejemplo MALIGNO =="
curl -s -X POST "$URL/predict" -H "Content-Type: application/json" -d '{
  "mean_radius": 17.99, "mean_texture": 10.38, "mean_perimeter": 122.8,
  "mean_area": 1001.0, "mean_smoothness": 0.1184, "mean_compactness": 0.2776,
  "mean_concavity": 0.3001, "mean_concave_points": 0.1471,
  "mean_symmetry": 0.2419, "mean_fractal_dimension": 0.07871 }'
echo
