from app.models.file import File
from app.schemas.file import FileCreateRequest
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session


class FileRepository:
    def create(self, db: Session, file: FileCreateRequest) -> FileResponse:
        db_file = File(**file.model_dump())
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        return db_file
