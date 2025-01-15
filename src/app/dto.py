from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class ApplicationDTO(BaseModel):
    id: UUID
    user_name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
