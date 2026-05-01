from typing import List, Dict


class PromptBuilder:

    def _split_sections(self, docs: List[Dict]):
        schema, joins, columns, examples, other = [], [], [], [], []

        for d in docs:
            t = d.get("type", "")

            if t == "table":
                schema.append(d["text"])
            elif t == "join":
                joins.append(d["text"])
            elif t == "column":
                columns.append(d["text"])
            elif t == "example":
                examples.append(d["text"])
            else:
                other.append(d["text"])

        return schema, joins, columns, examples, other

    def load_full_schema(self):
        with open("data/processed/schema_texts.txt", "r") as f:
            lines = f.readlines()

        cleaned = []
        seen = set()

        for l in lines:
            l = l.strip()
            if l and l not in seen:
                cleaned.append(l)
                seen.add(l)

        return "\n".join(cleaned)

    
    def build_prompt(self, question: str, retrieved_docs: List[Dict]) -> str:

        schema, joins, columns, examples, other = self._split_sections(retrieved_docs)

        full_schema = self.load_full_schema()

        context = list(set(schema + joins + columns + other))
        context_text = "\n".join(context)

        examples = examples[:2]
        example_text = "\n\n".join(examples)

        prompt = f"""
You are a PostgreSQL SQL expert.

### DATABASE SCHEMA:
{full_schema}

### RETRIEVED CONTEXT:
{context_text}

### EXAMPLES:
{example_text}

### RULES:
- Use only tables and columns from schema
- Use correct joins
- Use GROUP BY when needed
- Do not explain
- Return only SQL

### QUESTION:
{question}

### SQL:
"""
        return prompt.strip()

    
    def build_chat_prompt(self, messages: List[Dict], retrieved_docs: List[Dict]) -> str:

        schema, joins, columns, examples, other = self._split_sections(retrieved_docs)

        full_schema = self.load_full_schema()

        context = list(set(schema + joins + columns + other))
        context_text = "\n".join(context)

        examples = examples[:2]
        example_text = "\n\n".join(examples)

        # build chat history
        history = ""
        for m in messages:
            role = m.get("role")
            content = m.get("content")

            if role == "user":
                history += f"User: {content}\n"
            else:
                history += f"Assistant: {content}\n"

        prompt = f"""
You are a PostgreSQL SQL expert.

### DATABASE SCHEMA:
{full_schema}

### RETRIEVED CONTEXT:
{context_text}

### EXAMPLES:
{example_text}

### CHAT HISTORY:
{history}

### TASK:
Generate SQL for the LAST user request based on the conversation.

### RULES:
- Use only tables and columns from schema
- Use correct joins
- Use GROUP BY when needed
- Do not explain
- Return only SQL

### SQL:
"""

        return prompt.strip()