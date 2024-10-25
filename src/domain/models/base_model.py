from typing import Optional

from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    is_deleted: bool = Field(default=False, exclude=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, exclude=True)
