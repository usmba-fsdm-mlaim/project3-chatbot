# Utilisation d'une image Python officielle légère
FROM python:3.10-slim

# Définition du dossier de travail
WORKDIR /app

# Installation des dépendances système (si nécessaire pour certaines libs ML)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copie des requirements et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port
EXPOSE 8000

# Commande de lancement (FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]j