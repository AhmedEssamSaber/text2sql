from app.rag.retriever import Retriever
from app.core.config import settings

retriever = Retriever(
    index_path=settings.INDEX_PATH,
    texts_path=settings.TEXTS_PATH
)

results = retriever.retrieve("orders from germany", k=5)

for r in results:
    print(r)