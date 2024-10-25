from datetime import datetime
from typing import Optional

from sqlmodel import Field

from src.domain.models.base_model import BaseModel


class User(BaseModel, table=True):

    __tablename__ = "USER"

    name: str
    email: str = Field(sa_column_kwargs={"unique": True})
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
