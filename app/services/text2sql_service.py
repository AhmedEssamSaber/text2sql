from groq import Groq

from app.rag.retriever import Retriever
from app.llm.prompt_builder import PromptBuilder
from app.llm.generator import SQLGenerator
from app.core.config import settings

class Text2SQLService:

    def __init__(self, index_path: str, texts_path: str):

        self.retriever = Retriever(index_path, texts_path)
        self.prompt_builder = PromptBuilder()

        self.client = Groq(api_key=settings.GROQ_API_KEY)

        self.generator = SQLGenerator(client=self.client)

    def generate(self, question: str) -> str:

        docs = self.retriever.retrieve(question)

        prompt = self.prompt_builder.build_prompt(question, docs)

        sql = self.generator.generate(prompt)

        return sql