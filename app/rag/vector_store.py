# import faiss
# import pickle
# import numpy as np
# from typing import List

# class VectorStore:
#     def __init__(self, index_path: str, texts_path: str):
#         """
#         index_path: Path to faiss_index.bin.
#         texts_path: Path to texts.pkl.
#         """
#         self.index = faiss.read_index(index_path)

#         with open(texts_path, 'rb') as f:
#             self.texts = pickle.load(f)

#     def add(self, embeddings, texts):
#         """
#         Add new embeddings and their corresponding texts to the vector store (if we have a dynamic schema).
#         """
#         self.index.add(np.array(embeddings).astype('float32'))
#         self.texts.extend(texts)

#     def search(self, query_embedding: List[float], k: int = 5) -> List[str]:
#         """
#         Search for the top-k most similar documents.
#         """

#         query_embedding = np.array(query_embedding).astype('float32')
        
#         # make it 2D if it's 1D
#         if query_embedding.ndim == 1:
#             query_embedding = np.expand_dims(query_embedding, axis=0)
        
#         D, I = self.index.search(query_embedding, k)

#         results = []
#         for idx in I[0]:
#             results.append(self.texts[idx])
        
#         return results

import faiss
import pickle
import numpy as np
from typing import List, Tuple


class VectorStore:
    def __init__(self, index_path: str, texts_path: str):
        self.index = faiss.read_index(index_path)

        with open(texts_path, 'rb') as f:
            self.texts = pickle.load(f)

    def add(self, embeddings, texts):
        self.index.add(np.array(embeddings).astype('float32'))
        self.texts.extend(texts)

    def search(self, query_embedding: List[float], k: int = 5) -> Tuple[List[str], List[float]]:
        query_embedding = np.array(query_embedding).astype('float32')

        if query_embedding.ndim == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)

        D, I = self.index.search(query_embedding, k)

        results = []
        scores = []

        for idx, score in zip(I[0], D[0]):
            if idx == -1:
                continue
            results.append(self.texts[idx])
            scores.append(float(score))

        return results, scores