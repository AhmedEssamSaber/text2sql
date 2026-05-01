from app.utils.sql_validator import SQLValidator
from app.core.config import settings

class SQLGenerator:

    def __init__(self, client, model=settings.GENERATION_MODEL_NAME, temperature=0):
        self.client = client
        self.model = model
        self.temperature = temperature

    
    def generate(self, prompt: str) -> str:

        for _ in range(3):  # retry max 3 times
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature
                )

                sql = response.choices[0].message.content.strip()

                if SQLValidator.basic_check(sql):
                    return SQLValidator.fix_format(sql)

                print("Invalid SQL, retrying...")

            except Exception as e:
                print(f"API Error: {e}")

        print("Failed after retries → fallback")
        return "SELECT 1;"

