import os
import logging
import wandb
import torch
from typing import Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

class ModelLoader:
    """Service for loading and managing the NLP model using W&B Artifacts"""

    def __init__(self, artifact_address: Optional[str] = None):
        # Pull from Docker environment variable if not provided in code
        self.artifact_address = artifact_address or os.getenv("ARTIFACT_ADDRESS")

        self.model_path: Optional[str] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[AutoModelForCausalLM] = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # If no artifact_address, try local path
        if not self.artifact_address:
            local_path = os.path.join(os.path.dirname(__file__), "..", "..", "nlp", "models")
            if os.path.exists(local_path):
                self.artifact_address = local_path
                logger.info(f"Using local model path: {self.artifact_address}")
            else:
                logger.error("ARTIFACT_ADDRESS not found in environment or arguments, and local path not found!")
    def is_loaded(self) -> bool:
        """Checks if both the model and tokenizer are initialized"""
        return self.model is not None and self.tokenizer is not None
    def download_artifact(self) -> str:
        """Downloads the model artifact from W&B using the API key from Docker env, or returns local path"""
        print("wandb_api_key: ", os.getenv("WANDB_API_KEY"))
        # If artifact_address is a local path, return it directly
        if os.path.exists(self.artifact_address):
            logger.info(f"Using local artifact path: {self.artifact_address}")
            return self.artifact_address

        if not os.getenv("WANDB_API_KEY"):
            raise EnvironmentError("WANDB_API_KEY is missing. Check your .env/Docker setup.")

        logger.info(f"Fetching W&B Artifact: {self.artifact_address}")

        try:
            api = wandb.Api()
            artifact = api.artifact(self.artifact_address)
            artifact_dir = artifact.download()
            logger.info(f"Weights ready at: {artifact_dir}")
            return artifact_dir
        except Exception as e:
            logger.error(f"W&B Download failed: {e}")
            raise

    def load_model(self) -> bool:
        """Download and initialize model"""
        try:
            self.model_path = self.download_artifact()
            print("Model path: ", self.model_path)
            dtype = torch.float16 if self.device.type == "cuda" else torch.float32
            
            base_model_name = os.getenv("BASE_MODEL_NAME", "Qwen/Qwen2.5-0.5B")
            
            logger.info(f"Loading Base: {base_model_name} ({dtype})")
            self.model = AutoModelForCausalLM.from_pretrained(
                base_model_name,
                torch_dtype=dtype,
                trust_remote_code=True
            )

            # Check for LoRA
            if os.path.exists(os.path.join(self.model_path, "adapter_config.json")):
                logger.info("Applying LoRA Adapter...")
                self.model = PeftModel.from_pretrained(
                    self.model,
                    self.model_path,
                    torch_dtype=dtype
                )

            self.model = self.model.to(self.device)
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
            except:
                self.tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Load chat template if available
            chat_template_path = os.path.join(self.model_path, "chat_template.jinja")
            if os.path.exists(chat_template_path):
                try:
                    with open(chat_template_path, 'r') as f:
                        self.tokenizer.chat_template = f.read()
                    logger.info("Chat template loaded successfully")
                except Exception as e:
                    logger.warning(f"Failed to load chat template: {e}")
            else:
                # Set a default chat template if none exists
                logger.warning("No chat template found, using default")
                self.tokenizer.chat_template = "{% for message in messages %}{% if message['role'] == 'user' %}{{ '<|user|>\n' + message['content'] + '<|end|>\n<|assistant|>\n' }}{% elif message['role'] == 'assistant' %}{{ message['content'] + '<|end|>\n' }}{% endif %}{% endfor %}"

            logger.info("Model pipeline fully loaded.")
            return True

        except Exception as e:
            logger.error(f"Load Error: {str(e)}")
            return False
        