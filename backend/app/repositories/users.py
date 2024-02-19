from app.core.database import get_db
from app.models.user import User
from app.schemas.users import UserRegisterRequest, UserUpdateRequest
from fastapi import Depends
from sqlalchemy.orm import Session, joinedload


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self) -> list[User]:
        return self.db.query(User).options(joinedload(User.avatar)).all()

    def get_by_id(self, id: int) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == id)
            .options(joinedload(User.avatar))
            .first()
        )

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .options(joinedload(User.avatar))
            .first()
        )

    def create(self, user: UserRegisterRequest) -> User:
        db_user = User(**user.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user: User, payload: UserUpdateRequest) -> User:
        if payload.name:
            user.name = payload.name
        if payload.lastname:
            user.lastname = payload.lastname

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
