from typing import List
from app.rag.embedder import get_embedder
from app.rag.vector_store import VectorStore

class Retriever:
    def __init__(self, index_path: str, texts_path: str):
        self.vector_store = VectorStore(index_path, texts_path)
        self.embedder = get_embedder()

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        """
        Given a user query, retrieve the top-k most relevant documents.
        """

        # embed the query
        query_embedding = self.embedder.embed_query(query)
        
        # search in vector db
        results = self.vector_store.search(query_embedding, k)

        # clean the results by removing the "passage: " prefix
        cleaned_results = [
            r.replace("passage: ", "").strip() 
            for r in results
        ]

        return cleaned_results