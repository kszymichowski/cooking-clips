from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    owned_books = relationship("Ownership", back_populates="owner")
    followed_books = relationship("Follow", back_populates="follower")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

    recipes = relationship("Recipe", back_populates="book")
    ownerships = relationship("Ownership", back_populates="book")
    follows = relationship("Follow", back_populates="book")

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ingredients = Column(String)
    instructions = Column(String)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="recipes")
    video = relationship("Video", uselist=False, back_populates="recipe")

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))

    recipe = relationship("Recipe", back_populates="video")


class Ownership(Base):
    __tablename__ = "ownership"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    owner = relationship("User", back_populates="owned_books")
    book = relationship("Book", back_populates="ownerships")


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    can_edit = Column(Boolean)

    follower = relationship("User", back_populates="followed_books")
    book = relationship("Book", back_populates="follows")
