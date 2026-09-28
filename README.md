# Clasificador de tumores de mama con FastAPI y Docker

Proyecto individual de Machine Learning desplegado con Docker.

- **Problema:** clasificación binaria (0 = maligno, 1 = benigno)
- **Dataset:** Breast Cancer Wisconsin (incluido en scikit-learn), 10 características "mean"
- **Modelo:** `StandardScaler` + `LogisticRegression` (scikit-learn), guardado con `joblib`
- **API:** FastAPI (`/docs`, `/health`, `/model-info`, `/predict`)

> Proyecto académico. No es una herramienta de diagnóstico médico.

## Estructura

```
.
├── app.py                 # API FastAPI
├── train.py               # Entrenamiento del modelo
├── prepare_dataset.py     # Genera data/breast_cancer.csv
├── requirements.txt       # Dependencias con versiones fijas
├── Dockerfile
├── .dockerignore
├── data/breast_cancer.csv
├── models/model.joblib    # Se genera con train.py
├── tests/predict_examples.sh
└── practicas/             # Prácticas del curso
```

## Cómo reproducirlo

```bash
# 1. Entorno virtual con las MISMAS versiones que usará Docker
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Dataset y entrenamiento
python prepare_dataset.py
python train.py                   # crea models/model.joblib

# 3. Docker
docker build -t cancer-predictor:v1 .
docker images
docker run -d -p 8000:8000 --name cancer-api cancer-predictor:v1
docker ps

# 4. Probar
#   Navegador: http://localhost:8000/docs
bash tests/predict_examples.sh
docker logs cancer-api
```

## Ejemplo de predicción

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{
  "mean_radius": 13.03, "mean_texture": 18.42, "mean_perimeter": 82.61,
  "mean_area": 523.8, "mean_smoothness": 0.08983, "mean_compactness": 0.03766,
  "mean_concavity": 0.02562, "mean_concave_points": 0.02923,
  "mean_symmetry": 0.1467, "mean_fractal_dimension": 0.05863 }'
```

Respuesta esperada (los decimales pueden variar ligeramente):

```json
{"prediction": "benigno", "prediction_index": 1, "confidence": 0.98, "probabilities": {"maligno": 0.02, "benigno": 0.98}}
```

## Comandos útiles

```bash
docker stop cancer-api && docker rm cancer-api      # detener y eliminar
docker run -d -p 8001:8000 --name cancer-api-2 cancer-predictor:v1   # otro puerto del host
docker save -o cancer-predictor.tar cancer-predictor:v1               # exportar imagen
docker load -i cancer-predictor.tar                                    # importar imagen
```
