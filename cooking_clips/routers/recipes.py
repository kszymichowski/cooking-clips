from fastapi import HTTPException, Depends, APIRouter, status, UploadFile, File, Form
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
)

@router.post("/", response_model=schemas.Recipe)
async def create_recipe(
    name: str = Form(...),
    ingredients: str = Form(...),
    instructions: str = Form(...),
    book_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
    ):

    recipe_data = schemas.RecipeCreate(
        name=name,
        ingredients=ingredients,
        instructions=instructions,
        book_id=book_id
    )

    is_owner = db.query(models.Ownership).filter(
        models.Ownership.book_id == recipe_data.book_id,
        models.Ownership.user_id == current_user.id
        ).first()
    is_follower = db.query(models.Follow).filter(
        models.Follow.book_id == recipe_data.book_id,
        models.Follow.user_id == current_user.id
        ).first()

    if not is_owner and (not is_follower or not is_follower.can_edit):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user cannot add recipe: not an owner ors no edit rights")
    print("here 1")

    db_recipe = models.Recipe(
        name=recipe_data.name,
        ingredients=recipe_data.ingredients,
        instructions=recipe_data.instructions,
        book_id=recipe_data.book_id
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    print("here")

    # download video and put on local storage
    file_storage_service: Type[FileStorage] = LocalFileStorage()
    upload_path = Path(__file__).resolve().parent.parent.parent / "local_storage"


    file_bytes = await file.read()
    file_path = upload_path / file.filename
    print(file_path)
    file_storage_service.upload_file(file_path=file_path, file=file_bytes)

    db_video = models.Video(
       url=file_path,
       recipe_id=db_recipe.id 
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)


    return db_recipe