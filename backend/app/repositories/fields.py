from app.core.database import get_db
from app.models.field import Field
from app.models.user import User
from app.schemas.fields import FieldCreateSchema
from fastapi import Depends
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

    def get_count_by_name(self, name: str) -> int:
        return self.db.query(Field).filter(Field.name == name).count()

    def create(self, payload: FieldCreateSchema, owner: User) -> Field:
        field = Field(**payload.model_dump(), owner=owner)
        self.db.add(field)
        self.db.commit()
        self.db.refresh(field)

        return field
