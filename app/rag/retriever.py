# from typing import List
# from app.rag.embedder import get_embedder
# from app.rag.vector_store import VectorStore

# class Retriever:
#     def __init__(self, index_path: str, texts_path: str):
#         self.vector_store = VectorStore(index_path, texts_path)
#         self.embedder = get_embedder()

#     def retrieve(self, query: str, k: int = 5) -> List[str]:
#         """
#         Given a user query, retrieve the top-k most relevant documents.
#         """

#         # embed the query
#         query_embedding = self.embedder.embed_query(query)
        
#         # search in vector db
#         results = self.vector_store.search(query_embedding, k)

#         # clean the results by removing the "passage: " prefix
#         cleaned_results = [
#             r.replace("passage: ", "").strip() 
#             for r in results
#         ]

#         return list(set(cleaned_results))

from typing import List, Dict
from app.rag.embedder import get_embedder
from app.rag.vector_store import VectorStore


class Retriever:
    def __init__(self, index_path: str, texts_path: str):
        self.vector_store = VectorStore(index_path, texts_path)
        self.embedder = get_embedder()

    def _classify(self, text: str) -> str:
        """
        Classify retrieved text into types for better prompt structuring.
        """

        if text.startswith("Question:"):
            return "example"

        if "joins" in text or "Join condition" in text or "=" in text:
            return "join"

        if text.startswith("Table"):
            return "table"

        if "represents" in text:
            return "column"

        return "other"

    def retrieve(self, query: str, k: int = 15) -> List[Dict]:
        """
        Retrieve diverse and relevant chunks (schema + joins + examples).
        """

        query_embedding = self.embedder.embed_query(query)

        results, scores = self.vector_store.search(query_embedding, k)

        output = []
        seen_texts = set()
        seen_types = set()

        for text, score in zip(results, scores):
            cleaned = text.replace("passage: ", "").strip()

            if cleaned in seen_texts:
                continue

            seen_texts.add(cleaned)

            # classify
            t = self._classify(cleaned)

            # 🔥 enforce diversity (important)
            if t in seen_types and t != "example":
                continue

            seen_types.add(t)

            # 🔥 boost joins
            if t == "join":
                score += 0.15

            output.append({
                "text": cleaned,
                "score": float(score),
                "type": t
            })

        # sort by score
        output = sorted(output, key=lambda x: x["score"], reverse=True)

        return output