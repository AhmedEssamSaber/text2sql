from fastapi import APIRouter

from app.api.schemas import QueryRequest, QueryResponse
from app.services.text2sql_service import Text2SQLService
from app.core.config import settings


router = APIRouter()

service = Text2SQLService(
    index_path=settings.INDEX_PATH,
    texts_path=settings.TEXTS_PATH
)


@router.get("/")
def home():
    return {"message": "Text2SQL API is running"}


@router.post("/generate", response_model=QueryResponse)
def generate_sql(req: QueryRequest):

    sql = service.generate(req.question)

    return {"sql": sql}