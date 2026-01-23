import os
import logging
from typing import Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

logger = logging.getLogger(__name__)

class ModelLoader:
    """Service for loading and managing the NLP model"""

    # CORRECTION DU CHEMIN ICI : on remonte d'un cran avec ".."
    def __init__(self, model_path: str = "../nlp/models"):
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

            # 1. Load base model (Qwen)
            base_model_name = "Qwen/Qwen2.5-0.5B"
            logger.info(f"Loading base model: {base_model_name}")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                base_model_name,
                torch_dtype=dtype,
                trust_remote_code=True
            )

            # 2. Try Load LoRA adapter (SECURISE)
            # On vérifie d'abord si le fichier de config existe
            adapter_config_path = os.path.join(self.model_path, "adapter_config.json")
            
            if os.path.exists(adapter_config_path):
                logger.info(f"Found LoRA adapter at {self.model_path}. Loading...")
                try:
                    self.model = PeftModel.from_pretrained(
                        self.model,
                        self.model_path,
                        torch_dtype=dtype
                    )
                    logger.info("LoRA adapter loaded successfully.")
                except Exception as e:
                    logger.error(f"Error loading LoRA adapter: {e}")
                    logger.warning("Continuing with Base Model only.")
            else:
                logger.warning(f"⚠️ No LoRA adapter found at '{self.model_path}'. Using Base Model only.")

            # Move model to device
            self.model = self.model.to(self.device)

            # 3. Load tokenizer
            logger.info("Loading tokenizer...")
            # On essaie de charger le tokenizer local, sinon on prend celui du base model
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_path, 
                    trust_remote_code=True
                )
            except:
                logger.info("Local tokenizer not found, loading from base model...")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    base_model_name,
                    trust_remote_code=True
                )

            # Set pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            logger.info("✅ Model pipeline loaded successfully")
            return True

        except Exception as e:
            logger.error(f"❌ CRITICAL: Failed to load model: {str(e)}")
            # Pour le debug, on affiche l'erreur complète
            import traceback
            traceback.print_exc()
            return False

    def is_loaded(self) -> bool:
        """Check if the model is loaded"""
        return self.model is not None and self.tokenizer is not None