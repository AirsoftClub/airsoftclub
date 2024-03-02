from app.core.database import get_db
from app.models.field import Field
from app.models.user import User
from app.schemas.fields import FieldCreateSchema
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session


class FieldRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self):
        return self.db.query(Field).all()

    def get_by_id(self, id: int):
        return self.db.query(Field).filter(Field.id == id).first()

    def update(self, field: Field):
        self.db.add(field)
        self.db.commit()
        self.db.refresh(field)
        return field

    def get_all_by_distance(
        self, latitude: float, longitude: float, limit: int
    ) -> list[tuple[Field, float]]:
        distance = (
            func.acos(
                func.sin(func.radians(latitude))
                * func.sin(func.radians(Field.latitude))
                + func.cos(func.radians(latitude))
                * func.cos(func.radians(Field.latitude))
                * func.cos(func.radians(longitude) - func.radians(Field.longitude))
            )
            * 6371  # Earth's radius in kilometers
        )

        stmt = (
            select(Field, distance.label("distance"))
            .where(Field.deleted_at.is_(None))
            .order_by(distance.asc())
            .limit(limit)
        )

        return self.db.execute(stmt).all()

    def get_count_by_name(self, name: str) -> int:
        return self.db.query(Field).filter(Field.name == name).count()

    def create(self, payload: FieldCreateSchema, owner: User) -> Field:
        field = Field(**payload.model_dump(), owner=owner)
        self.db.add(field)
        self.db.commit()
        self.db.refresh(field)

        return field
