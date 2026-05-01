from groq import Groq

from app.rag.retriever import Retriever
from app.llm.prompt_builder import PromptBuilder
from app.llm.generator import SQLGenerator
from app.core.config import settings
from app.services.sql_executor import SQLExecutor
from app.llm.explainer import SQLExplainer
from app.utils.cache import SimpleCache

class Text2SQLService:

    def __init__(self, index_path: str, texts_path: str):

        self.retriever = Retriever(index_path, texts_path)
        self.prompt_builder = PromptBuilder()

        self.client = Groq(api_key=settings.GROQ_API_KEY)

        self.generator = SQLGenerator(client=self.client)

        self.executor = SQLExecutor()

        self.explainer = SQLExplainer(client=self.client)

        self.cache = SimpleCache(ttl=300)

        self.memory = []
        self.max_memory = 5
        
    
    def generate(self, question: str):

        # check cache first
        cached = self.cache.get(question)
        if cached:
            return {
                **cached,
                "cached": True
            }

        docs = self.retriever.retrieve(question)
        prompt = self.prompt_builder.build_prompt(question, docs)

        sql = self.generator.generate(prompt)
        sql = self.apply_limit(sql)
        
        result = self.executor.execute(sql)
        explanation = self.explainer.explain(question, sql)

        response = {
            "sql": sql,
            "result": result,
            "explanation": explanation
        }

        # save in cache
        self.cache.set(question, response)

        return {
            **response,
            "cached": False
        }

  
    def explain(self, question: str, sql: str) -> str:
        return self.explainer.explain(question, sql)
    

    def rewrite_question(self, messages):

        conversation = ""
        for m in messages:
            conversation += f"{m['role']}: {m['content']}\n"

        prompt = f"""
Rewrite the last user query into a complete standalone question.

Conversation:
{conversation}

Return only the rewritten question.
"""

        rewritten = self.generator.generate(prompt)
        return rewritten.strip()

    def apply_limit(self, sql: str, limit: int = 50) -> str:

        sql_lower = sql.lower()

        if "limit" in sql_lower:
            return sql

        return sql.rstrip(";") + f" LIMIT {limit};"
    

    def add_to_memory(self, role, content):
        self.memory.append({"role": role, "content": content})

        # keep last N messages
        self.memory = self.memory[-self.max_memory:]

    def build_chat_context(self):

        context = ""
        for m in self.memory:
            context += f"{m['role']}: {m['content']}\n"

        return context
    

    def chat(self, messages):

        user_question = messages[-1]["content"]

        self.add_to_memory("user", user_question)

        conversation_context = self.build_chat_context()

        prompt = f"""
You are a system that converts conversations into a clear standalone SQL question.

Conversation:
{conversation_context}

Return ONLY a clear standalone question.
"""

        question = self.generator.generate(prompt)

        docs = self.retriever.retrieve(question)
        prompt = self.prompt_builder.build_prompt(question, docs)

        sql = self.generator.generate(prompt)
        sql = self.apply_limit(sql)

        result = self.executor.execute(sql)
        explanation = self.explainer.explain(question, sql)

        self.add_to_memory("assistant", sql)

        return {
            "sql": sql,
            "result": result,
            "explanation": explanation
        }

