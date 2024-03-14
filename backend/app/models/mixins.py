from datetime import datetime

from sqlalchemy import Column, DateTime


class TimeTracked:
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(
        DateTime,
        nullable=True,
    )
