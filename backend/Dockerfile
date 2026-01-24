# Utilisation d'une image Python officielle légère
FROM python:3.10-slim

# Définition du dossier de travail
WORKDIR /app

# Installation des dépendances système (si nécessaire pour certaines libs ML)
RUN apt-get update && apt-get install 
# comment to push the correct dockerfile

COPY requirements.txt .

# Installation avec montage de cache pour pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port
EXPOSE 8000

# Commande de lancement (FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


