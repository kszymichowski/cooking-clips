from fastapi import FastAPI
from . import models
from .routers import users, login, books, recipes, follows
from .database import engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(login.router)
app.include_router(books.router)
app.include_router(recipes.router)
app.include_router(follows.router)


# jeśli env = prod to użyc s3Filemanada
# jesli nie to uzycj locl file mansae 
