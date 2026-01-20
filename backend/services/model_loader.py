# Model loader service - simplified for demo
# In production, this would load from MLflow model registry

class MedicalChatbotModel:
    def __init__(self):
        # Mock model - in real implementation, load from MLflow
        self.is_loaded = True

    def predict(self, message: str) -> str:
        # Simple rule-based responses for medical assistant
        message_lower = message.lower()

        if "headache" in message_lower:
            return "For headaches, I recommend resting in a quiet, dark room and staying hydrated. If symptoms persist or worsen, please consult a healthcare professional."
        elif "fever" in message_lower:
            return "A fever indicates your body is fighting an infection. Monitor your temperature and consult a doctor if it exceeds 103°F (39.4°C) or lasts more than 3 days."
        elif "cough" in message_lower:
            return "Coughs can be caused by various factors. Stay hydrated, use a humidifier, and consider over-the-counter remedies. See a doctor if it persists."
        elif "pain" in message_lower:
            return "Pain can have many causes. Please describe your symptoms in more detail or consult a healthcare professional for proper diagnosis."
        else:
            return "I'm a medical assistant chatbot. I can help with general health questions, but I'm not a substitute for professional medical advice. Please consult a healthcare provider for personalized guidance."

# Global model instance
model = MedicalChatbotModel()

def load_model():
    """Load the model - placeholder for MLflow integration"""
    return model

def get_model():
    """Get the loaded model"""
    return model
