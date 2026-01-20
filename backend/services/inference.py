from services.model_loader import get_model

def get_chat_response(message: str) -> str:
    """
    Get chat response from the medical assistant model
    """
    model = get_model()
    return model.predict(message)
