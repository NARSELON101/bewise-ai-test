import uuid

from sqlalchemy import DateTime, String, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.postgresql.database import Base


class Application(Base):
    __tablename__ = 'application'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return (f"\n{self.id}\n{self.created_at}'\n{self.user_name}"
                f"\n{self.description}")
