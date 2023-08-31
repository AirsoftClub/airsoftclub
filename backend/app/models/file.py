from datetime import datetime

from app.models.base import Base
from sqlalchemy import Column, DateTime, Integer, String


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def url(self):
        return f"{self.path}"

    def __repr__(self):
        return f"<File {self.id}>"
