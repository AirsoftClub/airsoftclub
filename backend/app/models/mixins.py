from datetime import datetime

from sqlalchemy import Column, DateTime


class TimeTracked:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
