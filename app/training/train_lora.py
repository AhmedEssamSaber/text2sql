import json
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model


class QLoRATrainer:

    def __init__(self, model_name, data_path):
        self.model_name = model_name
        self.data_path = data_path

    def build_prompt(self, schema, question, sql):
        return f"""You are an expert SQL generator.

### Rules:
- Use only tables and columns from schema
- Return only SQL

### Database Schema:
{schema}

### User Question:
{question}

### SQL Query:
{sql}"""

    def load_data(self):
        with open(self.data_path, "r") as f:
            data = json.load(f)
        return Dataset.from_list(data)

    def preprocess(self, example):
        text = self.build_prompt(
            example["schema"],
            example["question"],
            example["sql"]
        )

        tokens = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=512
        )

        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    def setup(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4"
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto"
        )

        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )

        self.model = get_peft_model(self.model, lora_config)

    def train(self):
        dataset = self.load_data()
        dataset = dataset.map(self.preprocess)

        training_args = TrainingArguments(
            output_dir="models/qlora-output",
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            num_train_epochs=2,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=10,
            save_strategy="epoch",
            report_to="none"
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            data_collator=DataCollatorForLanguageModeling(self.tokenizer, mlm=False)
        )

        trainer.train()

        self.model.save_pretrained("models/qlora-adapter")
        self.tokenizer.save_pretrained("models/qlora-adapter")


if __name__ == "__main__":
    trainer = QLoRATrainer(
        model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        data_path="data/train.json"
    )
    trainer.setup()
    trainer.train()