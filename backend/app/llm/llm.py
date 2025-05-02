import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from jsonformer import Jsonformer

class HuggingFaceLLM:
    def __init__(self, temperature=0, top_k=50, model_name="mistralai/Mistral-7B-Instruct-v0.1"):
        print("Loading model... (this may take time on first run)")
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

        # Ensure pad_token_id is not the same as eos_token_id
        if self.tokenizer.pad_token_id is None or self.tokenizer.pad_token_id == self.tokenizer.eos_token_id:
            self.tokenizer.pad_token = self.tokenizer.eos_token + "_pad"
            self.tokenizer.pad_token_id = self.tokenizer.convert_tokens_to_ids(self.tokenizer.pad_token)

        self.top_k = top_k

    def generate(self, prompt, max_new_tokens=256):
        schema = {
            "type": "object",
            "properties": {
                "action": {"type": "string", "const": "restaurant_search"},
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "near": {"type": "string"},
                        "price": {"type": "string"},
                        "open_now": {"type": "boolean"}
                    },
                    "required": ["query", "near"]
                }
            },
            "required": ["action", "parameters"]
        }

        builder = Jsonformer(
            model=self.model,
            tokenizer=self.tokenizer,
            json_schema=schema,
            prompt=prompt,
        )

        print("Generating structured JSON...")
        try:
            result = builder()
            print("LLM output:", result)
            return result
        except Exception as e:
            print(f"JSON generation failed: {e}")
            return None
