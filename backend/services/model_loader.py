import os
import logging
from typing import Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

logger = logging.getLogger(__name__)


class ModelLoader:
    """Service for loading and managing the NLP model"""

    def __init__(self, model_path: str = "nlp/models"):
        self.model_path = model_path
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[AutoModelForCausalLM] = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")

    def load_model(self) -> bool:
        """Load the model and tokenizer from the specified path"""
        try:
            # Determine dtype based on device
            dtype = torch.float16 if self.device.type == "cuda" else torch.float32
            logger.info(f"Using dtype: {dtype} for device: {self.device}")

            # Load base model
            base_model_name = "Qwen/Qwen2.5-0.5B"
            logger.info(f"Loading base model: {base_model_name}")
            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_name,
                torch_dtype=dtype,
                trust_remote_code=True
            )

            # Load LoRA adapter
            logger.info(f"Loading LoRA adapter from: {self.model_path}")
            try:
                self.model = PeftModel.from_pretrained(
                    base_model,
                    self.model_path,
                    torch_dtype=dtype
                )
            except TypeError as e:
                logger.warning(f"Config incompatible, trying to load adapter manually: {e}")
                # Try to load the adapter weights manually
                from peft import LoraConfig
                from safetensors.torch import load_file

                # Create a minimal LoraConfig
                lora_config = LoraConfig(
                    r=16,
                    lora_alpha=32,
                    target_modules=["v_proj", "q_proj", "k_proj", "o_proj"],
                    lora_dropout=0.05,
                    bias="none",
                    task_type="CAUSAL_LM"
                )

                # Load the adapter weights
                adapter_weights = load_file(os.path.join(self.model_path, "adapter_model.safetensors"))

                # Create PeftModel manually
                from peft import get_peft_model
                self.model = get_peft_model(base_model, lora_config)

                # Load the state dict
                self.model.load_state_dict(adapter_weights, strict=False)

            # Move model to device
            self.model = self.model.to(self.device)

            # Load tokenizer
            logger.info("Loading tokenizer")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )

            # Set pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Set chat template if available
            chat_template_path = os.path.join(self.model_path, "chat_template.jinja")
            if os.path.exists(chat_template_path):
                with open(chat_template_path, 'r', encoding='utf-8') as f:
                    self.tokenizer.chat_template = f.read()
                logger.info("Chat template loaded")

            logger.info("Model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            return False

    def is_loaded(self) -> bool:
        """Check if the model is loaded"""
        return self.model is not None and self.tokenizer is not None