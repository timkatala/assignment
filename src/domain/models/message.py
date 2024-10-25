from sqlmodel import Field
from uuid import UUID

from src.domain.models.base_model import BaseModel


class Message(BaseModel, table=True):
    __tablename__ = "MESSAGE"

    sender_id: UUID = Field(foreign_key="USER.id")
    content: str
