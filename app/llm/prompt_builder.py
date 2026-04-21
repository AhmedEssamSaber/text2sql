from typing import List

class PromptBuilder:
    def __init__(self):
        pass

    def build_prompt(self, query: str, schema_chunks: List[str]) -> str:
        """
        Build a prompt for the LLM by combining the user query with relevant schema information.
        """

        schema_text = "\n\n".join(schema_chunks)

        prompt = f"""
You are an expert SQL generator.

Your task is to generate a correct SQL query based on the given database schema and user question.

### Example:
User Question: number of customers
SQL Query: SELECT COUNT(*) FROM customers;

### Rules:
- Use only the tables and columns provided in the schema
- Respect foreign key relationships when joining tables
- Do not invent tables or columns
- Use proper JOIN conditions based on foreign keys
- Use GROUP BY when aggregation is needed
- Return ONLY the SQL query without any explanation
- Use PostgreSQL syntax

### Database Schema:
{schema_text}

### User Question:
{query}

### SQL Query:
"""
        return prompt.strip() 