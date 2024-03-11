from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends()):

    is_owner = db.query(models.Ownership).filter(models.Ownership.book_id == recipe.book_id and models.Ownership.user_id == current_user.id).first()
    is_follower = db.query(models.Follow).filter(models.Follow.book_id == recipe.book_id and models.Follow.user_id == current_user.id).first()

    if not is_owner and (not is_follower or not is_follower.can_edit):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="book not found")

    db_recipe = models.Recipe(**recipe.model_dump())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe