from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message to send to the chatbot")
    max_length: Optional[int] = Field(100, ge=10, le=500, description="Maximum length of generated response")
    temperature: Optional[float] = Field(0.7, ge=0.1, le=2.0, description="Sampling temperature for generation")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Generated response from the chatbot")
    status: str = Field("success", description="Response status")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    status: str = Field("error", description="Response status")