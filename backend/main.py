import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router
from routes.health import router as health_router

# Configure logging for production monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('logs/app.log') if os.path.exists('logs') else logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Medical Assistant Chatbot API",
    version="1.0.0",
    description="Intelligent medical assistant with NLP capabilities"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development frontend
        "http://127.0.0.1:3000",  # Alternative localhost
        "*"  # In production, restrict to specific domains
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(health_router, prefix="/api", tags=["health"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Medical Assistant Chatbot API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health",
            "metrics": "/api/metrics"
        }
    }

@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("Starting Medical Assistant Chatbot API")
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("Shutting down Medical Assistant Chatbot API")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server on http://0.0.0.0:8000")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
