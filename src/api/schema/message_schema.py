from uuid import UUID

from pydantic import BaseModel


class MessageRequestBody(BaseModel):
    sender_id: UUID
    content: str
