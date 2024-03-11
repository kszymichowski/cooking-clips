from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..utils.auth import get_current_user


router = APIRouter(
    prefix="/follows",
    tags=["follows"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=schemas.Follow)
def create_follow(follow: schemas.FollowCreate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends()):
    db_follow = models.Follow(**follow.model_dump())
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow