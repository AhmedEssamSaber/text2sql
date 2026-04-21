# from app.rag.embedder import get_embedder  

# embedder = get_embedder()  

# texts = [  
#     "Table orders stores customer orders",  
#     "Table customers contains user data"  
# ]  

# query = "total orders per customer"  

# doc_embeddings = embedder.embed_documents(texts)  
# query_embedding = embedder.embed_query(query)  

# print("Doc embedding shape:", len(doc_embeddings), len(doc_embeddings[0]))  
# print("Query embedding shape:", len(query_embedding))
from app.rag.retriever import Retriever
from app.rag.prompt_builder import PromptBuilder
# paths
INDEX_PATH = r"D:\Ai courses\text2sql\data\faiss_index.bin"
TEXTS_PATH = r"D:\Ai courses\text2sql\data\texts.pkl"

retriever = Retriever(INDEX_PATH, TEXTS_PATH)
prompt_builder = PromptBuilder()

query = "total orders per customer"

schema = retriever.retrieve(query, k=3)

prompt = prompt_builder.build_prompt(query, schema)

print(prompt)