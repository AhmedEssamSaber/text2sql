from fastapi import APIRouter, HTTPException
import time
import logging

from app.services.text2sql_service import Text2SQLService
from app.core.config import settings
from app.api.schemas import QueryRequest, QueryResponse, ChatRequest

router = APIRouter()

logger = logging.getLogger(__name__)

# init service
service = Text2SQLService(
    index_path=settings.INDEX_PATH,
    texts_path=settings.TEXTS_PATH
)


# Routes
@router.get("/")
def home():
    return {"message": "Text2SQL API is running"}


@router.get("/health")
def health():
    return {"status": "ok"}


# GENERATE
@router.post("/generate", response_model=QueryResponse)
def generate_sql(request: QueryRequest):

    start_time = time.time()

    try:
        logger.info(f"Question: {request.question}")

       
        response = service.generate(request.question)

        execution_time = round(time.time() - start_time, 3)

        return QueryResponse(
            success=True,
            sql=response["sql"],
            result=response["result"],
            explanation=response["explanation"] if request.explain else None,
            execution_time=execution_time
        )

    except Exception as e:
        logger.error(f"Error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# CHAT (Multi-turn)
@router.post("/chat", response_model=QueryResponse)
def chat(request: ChatRequest):

    start_time = time.time()

    try:
        response = service.chat([m.dict() for m in request.messages])

        execution_time = round(time.time() - start_time, 3)

        return QueryResponse(
            success=True,
            sql=response["sql"],
            rows=len(response["result"]),
            result=response["result"],
            explanation=response["explanation"],
            execution_time=execution_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))