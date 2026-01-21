from fastapi import APIRouter
from services.model_loader import get_model

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    model = get_model()
    return {
        "status": "healthy",
        "message": "Medical Assistant Chatbot is running",
        "model_version": model.version,
        "model_loaded": model.is_loaded
    }

@router.get("/metrics")
async def get_metrics():
    """Get model performance metrics"""
    model = get_model()
    return {
        "model_metrics": model.get_metrics(),
        "model_version": model.version,
        "service_status": "operational"
    }
