from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import List
from .. import models
from .. import schemas
from ..database import get_db
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["users"],
    #dependencies=[Depends(get_token_header)],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    hash_pass = pwd_context.hash(request.password)
    db_user = models.User(username=request.username, password=hash_pass, email=request.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user