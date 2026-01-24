from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
from services.model_loader import ModelLoader
from services.inference import InferenceService

logger = logging.getLogger(__name__)

router = APIRouter()

# Global references to services (will be set by chat.py initialization)
model_loader = None
inference_service = None


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify backend and model status.

    Returns:
        - status: "healthy" if everything is working
        - model_loaded: boolean indicating if model is loaded
        - inference_ready: boolean indicating if inference service is ready
    """
    try:
        # Check if model is loaded
        model_loaded = model_loader.is_loaded()

        # Check if inference service is initialized
        inference_ready = hasattr(inference_service, 'generator') and inference_service.generator is not None

        status = "healthy" if model_loaded and inference_ready else "unhealthy"

        response = {
            "status": status,
            "model_loaded": model_loaded,
            "inference_ready": inference_ready,
            "service": "chatbot-backend"
        }

        logger.info(f"Health check: {status}")
        return JSONResponse(content=response, status_code=200 if status == "healthy" else 503)

    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return JSONResponse(
            content={
                "status": "error",
                "error": str(e),
                "service": "chatbot-backend"
            },
            status_code=500
        )