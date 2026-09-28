# Imagen base ligera de Python
FROM python:3.11-slim

# Logs sin buffer (para verlos de inmediato con "docker logs") y sin .pyc
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# 1) Primero requirements.txt: aprovecha la cache de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Despues el codigo y el modelo ya entrenado
COPY app.py .
COPY models/ ./models/

# Documenta el puerto en el que escucha FastAPI (se publica con -p)
EXPOSE 8000

# Arranca la API escuchando en todas las interfaces del contenedor
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
