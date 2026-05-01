import torch
from sentence_transformers import SentenceTransformer
from typing import List
from app.core.config import settings


class BGEEmbedder:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL_NAME,
            device=self.device
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents into vector representations.
        """

        texts = [f'passage: {t}' for t in texts]

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a query into a vector representation.
        """

        query = f'query: {query}'

        embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        return embedding.tolist()


_embedder = None


def get_embedder() -> 'BGEEmbedder':
    global _embedder
    if _embedder is None:
        _embedder = BGEEmbedder()
    return _embedder