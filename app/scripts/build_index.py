import os
import pickle
import faiss
import numpy as np

from app.rag.schema_loader import schema_to_text
from app.rag.embedder import get_embedder
from app.rag.example_loader import load_examples

import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "embeddings")

os.makedirs(DATA_DIR, exist_ok=True)


def main():
    print("Loading schema from JSON...")

    
    with open(os.path.join(BASE_DIR, "data", "processed", "schema.json"), "r") as f:
        schema = json.load(f)

    print("Converting schema to text...")
    schema_texts = schema_to_text(schema)

    print("Loading examples...")
    example_texts = load_examples(
        os.path.join(BASE_DIR, "data", "processed", "few-shots.json")
    )

    # combine schema + examples
    all_texts = schema_texts + example_texts

    print(f"Total chunks: {len(all_texts)}")

    embedder = get_embedder()

    print("Generating embeddings...")
    embeddings = embedder.embed_documents(all_texts)

    embeddings = np.array(embeddings).astype("float32")

    print("Building FAISS index...")
    dim = embeddings.shape[1]

    # cosine similarity
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print("Saving index...")
    faiss.write_index(index, os.path.join(DATA_DIR, "faiss_index.bin"))

    print("Saving texts...")
    with open(os.path.join(DATA_DIR, "texts.pkl"), "wb") as f:
        pickle.dump(all_texts, f)

    print("RAG index built successfully!")


if __name__ == "__main__":
    main()