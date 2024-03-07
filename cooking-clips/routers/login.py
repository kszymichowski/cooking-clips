from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..utils.auth import generate_token
from ..database import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Login"],
    prefix="/login"
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/")
def auth_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == request.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")
    
    if not pwd_context.verify(request.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = generate_token(data={"sub": db_user.username, "id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}

