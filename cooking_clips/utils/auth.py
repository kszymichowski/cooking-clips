import os
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
import datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import os

SECRET_KEY = None
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def set_secret_key():
    global SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY')

def generate_token(data: dict):
    if not SECRET_KEY:
        set_secret_key()
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not SECRET_KEY:
        set_secret_key()
    try:
        jwt_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = jwt_payload.get("sub")
        id: int = jwt_payload.get("id")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not find user", headers={'WWW-Authenticate': 'Bearer'})
        token_data = schemas.TokenData(username=username, id=id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={'WWW-Authenticate': 'Bearer'})
    return token_data