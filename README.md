# 🤖 Intelligent Chatbot System  
**DevOps & MLOps Project**

---

## Project Overview

The **Intelligent Chatbot System** is an end-to-end AI application designed to demonstrate **modern DevOps and MLOps practices**.  
The system provides a conversational chatbot capable of understanding user intents and responding appropriately, while being fully automated, scalable, monitored, and continuously improvable.

This project follows the **Scrum methodology** and showcases:
- NLP model development
- Full-stack application (Frontend + Backend)
- CI/CD automation
- Kubernetes deployment
- Monitoring and observability
- Automated model retraining pipeline (MLOps)

---

## Project Objectives

- Build an NLP-based chatbot for customer interaction
- Expose the chatbot through a REST API
- Provide a web-based chat interface
- Track and version ML models using MLflow
- Automate deployment with CI/CD pipelines
- Deploy on Kubernetes with scalability
- Monitor system and model performance
- Implement an automated retraining pipeline

## Main Features

- REST API with `/chat` and `/health` endpoints
- Web-based chatbot interface
- ML experiment tracking and model registry
- Dockerized services
- CI/CD pipeline with automated tests and deployment
- Kubernetes-based deployment (scalable & resilient)
- Monitoring dashboards and alerts
- Automated model retraining and promotion

## Project Structure
```text
intelligent-chatbot/
│
├── README.md
├── .gitignore
├── docker-compose.yml
│
├── backend/                      # Backend API (FastAPI)
│   ├── app/
│   │   ├── main.py               # FastAPI entry point
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── chat.py        # /chat endpoint
│   │   │   │   ├── health.py      # /health endpoint
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── inference.py       # Model inference logic
│   │   │   ├── model_loader.py    # Load model from MLflow
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py          # Environment variables
│   │   │   └── logging.py
│   │   └── __init__.py
│   ├── tests/
│   │   ├── test_chat.py
│   │   └── test_health.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                     # Web-based Chat Interface
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatUI.jsx
│   │   ├── services/
│   │   │   └── api.js             # Backend API calls
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── ml/                           # Machine Learning & MLOps
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   ├── training/
│   │   ├── train.py               # Initial training
│   │   ├── evaluate.py
│   │   └── preprocessing.py
│   ├── retraining/
│   │   ├── retrain.py             # Automated retraining
│   │   ├── compare_models.py      # New vs production model
│   │   └── promote_model.py       # MLflow model promotion
│   ├── mlflow/
│   │   └── mlflow_tracking.py
│   └── requirements.txt
│
├── cicd/                         # CI/CD Pipelines
│   ├── github-actions/
│   │   └── pipeline.yml
│   └── scripts/
│       ├── deploy.sh
│       └── rollback.sh
│
├── k8s/                          # Kubernetes Manifests
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
│
├── monitoring/                   # Monitoring & Observability
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   └── dashboards/
│   └── alerts/
│       └── alert-rules.yml
