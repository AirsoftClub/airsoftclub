from app.models.field import Field
from sqlalchemy.orm import Session


class FieldRepository:
    def get_all(self, db: Session):
        return db.query(Field).all()

    def get_by_id(self, db: Session, id: int):
        return db.query(Field).filter(Field.id == id).first()
