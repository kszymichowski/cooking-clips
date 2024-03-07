from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    owned_books: List["Ownership"] = []
    followed_books: List["Follow"] = []

    class Config:
        orm_mode = True

class OwnershipBase(BaseModel):
    user_id: int
    book_id: int

class OwnershipCreate(OwnershipBase):
    pass

class Ownership(OwnershipBase):
    id: int
    owner: User

    class Config:
        orm_mode = True

class FollowBase(BaseModel):
    user_id: int
    book_id: int

class FollowCreate(FollowBase):
    pass

class Follow(FollowBase):
    id: int
    follower: User

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    name: str
    ingredients: str
    instructions: str

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    book_id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    recipes: List[Recipe] = []

    class Config:
        orm_mode = True

class VideoBase(BaseModel):
    url: str

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class UserAuthenticate(BaseModel):
    username: str
    password: str

class UserAuthenticateResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None