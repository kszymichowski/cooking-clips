from fastapi import HTTPException, Depends, APIRouter, status, UploadFile, File
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..utils.auth import get_current_user
from ..file_service.files import FileStorage, LocalFileStorage
from typing import Type
from pathlib import Path

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, file: UploadFile = File() , db: Session = Depends(get_db), current_user: schemas.TokenData = Depends()):

    is_owner = db.query(models.Ownership).filter(models.Ownership.book_id == recipe.book_id and models.Ownership.user_id == current_user.id).first()
    is_follower = db.query(models.Follow).filter(models.Follow.book_id == recipe.book_id and models.Follow.user_id == current_user.id).first()

    if not is_owner and (not is_follower or not is_follower.can_edit):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="book not found")

    db_recipe = models.Recipe(**recipe.model_dump())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    # download video and put on local storage
    file_storage_service: Type[FileStorage] = LocalFileStorage
    upload_path = Path(__file__).resolve().parent.parent / "local_storage"


    file_bytes = file.read()
    file_path = upload_path / file.filename
    print(file_path)
    file_storage_service.upload_file(file_path, file_bytes)


    return db_recipe