from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class SQLGenerator:
    def __init__(self, model_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        self.model.eval()

    def generate(self, prompt, max_new_tokens=150):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )

        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        if "### SQL Query:" in result:
            return result.split("### SQL Query:")[-1].strip()

        return result.strip()