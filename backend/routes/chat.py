from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
from backend.schemas.chat import ChatRequest, ChatResponse, ErrorResponse
from backend.services.model_loader import ModelLoader
from backend.services.inference import InferenceService
from backend.routes import health

logger = logging.getLogger(__name__)

router = APIRouter()

# Global services (in production, use dependency injection)
model_loader = ModelLoader()
inference_service = InferenceService(model_loader)

# Set references in health module
health.model_loader = model_loader
health.inference_service = inference_service

# Initialize model on startup
@router.on_event("startup")
async def startup_event():
    """Initialize model and inference service on startup"""
    logger.info("Initializing model and inference service...")
    if model_loader.load_model():
        inference_service.initialize_generator()
        logger.info("Model initialization completed successfully")
    else:
        logger.error("Failed to initialize model")
        raise RuntimeError("Model initialization failed")


@router.post("/chat", response_model=ChatResponse, responses={500: {"model": ErrorResponse}})
async def chat(request: ChatRequest):
    """
    Process a chat message and return a response from the chatbot.

    - **message**: The user's message (1-1000 characters)
    - **max_length**: Maximum response length (10-500, default: 100)
    - **temperature**: Sampling temperature (0.1-2.0, default: 0.7)
    """
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")

        # Generate response
        response = inference_service.generate_response(
            message=request.message,
            max_length=request.max_length,
            temperature=request.temperature
        )

        if response is None:
            raise HTTPException(status_code=500, detail="Failed to generate response")

        logger.info(f"Generated response: {response[:50]}...")
        return ChatResponse(response=response, status="success")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")