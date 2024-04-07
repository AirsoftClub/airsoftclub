import datetime

from sqlalchemy import Column, DateTime


class TimeTracked:
    created_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.UTC),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.UTC),
        onupdate=datetime.datetime.now(datetime.UTC),
        nullable=False,
    )
    deleted_at = Column(
        DateTime,
        nullable=True,
    )
