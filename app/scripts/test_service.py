from app.services.text2sql_service import Text2SQLService
from app.core.config import settings


service = Text2SQLService(
    index_path=settings.INDEX_PATH,
    texts_path=settings.TEXTS_PATH
)

questions = [
    "list all customers from germany",
    "customers who never placed orders",
    "total revenue from usa in 2024",
    "top 5 products by quantity sold"
]

for q in questions:
    print("Q:", q)
    sql = service.generate(q)
    print("SQL:", sql)
    print("-" * 50)