from pydantic import BaseModel
from typing import List, Optional, Any


# Chat 
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# Query
class QueryRequest(BaseModel):
    question: str
    explain: Optional[bool] = True
    limit: Optional[int] = 50


class QueryResponse(BaseModel):
    success: bool
    sql: str
    result: List[Any]
    explanation: Optional[str] = None
    execution_time: float
    cached: Optional[bool] = False
    rows: Optional[int] = None