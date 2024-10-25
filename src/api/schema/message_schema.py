from typing import List
from uuid import UUID

from pydantic import BaseModel

from src.domain.models import Message


class MessageRequestBody(BaseModel):
    sender_id: UUID
    content: str


class PaginatedMessageResponse(BaseModel):
    count: int
    messages: List[Message]
