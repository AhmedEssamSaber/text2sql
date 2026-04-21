from app.rag.retriever import Retriever
from app.llm.prompt_builder import PromptBuilder
from app.llm.generator import SQLGenerator

INDEX_PATH = r"D:\Ai courses\text2sql\data\embeddings\faiss_index.bin"
TEXTS_PATH = r"D:\Ai courses\text2sql\data\embeddings\texts.pkl"

retriever = Retriever(INDEX_PATH, TEXTS_PATH)
prompt_builder = PromptBuilder()
generator = SQLGenerator()

query = "total orders per customer"

schema = retriever.retrieve(query, k=3)

prompt = prompt_builder.build_prompt(query, schema)

sql = generator.generate(prompt)

print(sql)