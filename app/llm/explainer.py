from app.core.config import settings

class SQLExplainer:
    def __init__(self, client, model=settings.GENERATION_MODEL_NAME):
        self.client = client
        self.model = model

    def explain(self, question: str, sql: str) -> str:

        prompt = f"""
Explain this SQL query in 3-4 short sentences only.

Be concise and do not give examples or step-by-step breakdown.
Ignore LIMIT clauses.

Question:
{question}

SQL:
{sql}

Explanation:
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content.strip()