from app.rag.embedder import get_embedder  

embedder = get_embedder()  

texts = [  
    "Table orders stores customer orders",  
    "Table customers contains user data"  
]  

query = "total orders per customer"  

doc_embeddings = embedder.embed_documents(texts)  
query_embedding = embedder.embed_query(query)  

print("Doc embedding shape:", len(doc_embeddings), len(doc_embeddings[0]))  
print("Query embedding shape:", len(query_embedding))