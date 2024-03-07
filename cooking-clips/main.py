from fastapi import FastAPI
from . import models
from .routers import users, login, books, recipes
from .database import engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(login.router)
app.include_router(books.router)
app.include_router(recipes.router)
