from app.rag.retriever import Retriever
from app.llm.prompt_builder import PromptBuilder
from app.llm.generator import SQLGenerator

class Text2SQLService:
    def __init__(self, index_path: str, texts_path: str):
        self.retriever = Retriever(index_path, texts_path)
        self.prompt_builder = PromptBuilder()
        self.generator = SQLGenerator()

    def generate_sql(self, query: str, k: int = 3) -> str:
        print("Step 1: Retrieval...")
        schema_chunks = self.retriever.retrieve(query, k=k)

        print("Step 2: Prompt...")
        prompt = self.prompt_builder.build_prompt(query, schema_chunks)

        print("Step 3: Generation...")
        raw_output = self.generator.generate(prompt)

        print("Step 4: Cleaning...")
        sql = self._clean_sql(raw_output)

        return sql
        
    def _clean_sql(self, text: str) -> str:
        """
        Clean the raw output from the LLM to extract the SQL query.
        """

        # remove everything before SQL Query:
        if "SQL Query:" in text:
            text = text.split("SQL Query:")[-1]

        text = text.strip()

        # cut after first ;
        if ";" in text:
            text = text.split(";")[0] + ";"

        return text