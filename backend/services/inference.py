import logging
from typing import Optional
import torch
from transformers import pipeline
from backend.services.model_loader import ModelLoader

logger = logging.getLogger(__name__)


class InferenceService:
    """Service for running inference with the loaded model"""

    def __init__(self, model_loader: ModelLoader):
        self.model_loader = model_loader
        self.generator = None

    def initialize_generator(self):
        """Initialize the text generation pipeline"""
        if not self.model_loader.is_loaded():
            raise ValueError("Model not loaded. Call model_loader.load_model() first.")

        try:
            # Use the model directly for generation since PeftModel is not supported in pipeline
            self.generator = self.model_loader.model
            logger.info("Inference model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize inference model: {str(e)}")
            raise

    def generate_response(self, message: str, max_length: int = 100, temperature: float = 0.7) -> Optional[str]:
        """Generate a response to the user's message"""
        if not self.generator:
            raise ValueError("Generator not initialized. Call initialize_generator() first.")

        try:
            # Use proper chat template
            messages = [{"role": "user", "content": message}]
            prompt = self.model_loader.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

            # Tokenize input
            inputs = self.model_loader.tokenizer(prompt, return_tensors="pt").to(self.model_loader.device)

            # Calculate max_new_tokens (total length - input length)
            input_length = inputs['input_ids'].shape[1]
            max_new_tokens = max_length - input_length

            # Generate response
            with torch.no_grad():
                outputs = self.generator.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    do_sample=True,
                    eos_token_id=self.model_loader.tokenizer.eos_token_id,
                    pad_token_id=self.model_loader.tokenizer.pad_token_id,
                    num_return_sequences=1
                )

            # Decode the generated tokens
            generated_text = self.model_loader.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)

            # Clean up the response
            response = generated_text.strip()

            logger.info(f"Generated response of length {len(response)}")
            return response

        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")
            return None
