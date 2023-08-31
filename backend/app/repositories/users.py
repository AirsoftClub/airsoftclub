from app.models.user import User
from app.schemas.users import UserRegisterRequest
from sqlalchemy.orm import Session


class UserRepository:
    def get_all(self, db: Session) -> list[User]:
        return db.query(User).all()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user: UserRegisterRequest) -> User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
