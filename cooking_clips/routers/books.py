from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..utils.auth import get_current_user


router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends()):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    db_owner = models.Ownership(
        user_id = current_user.id,
        book_id = db_book.id
    )
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)

    return db_book

@router.get("{book_id}/", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends()):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("{user_id}/follows")
def get_followed_books_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_followed = db.query(models.Follow).filter(models.Follow.user_id == user_id).all()
    if db_followed is None:
        raise HTTPException(status_code=404, detail="Followed books or user not found")
    
    db_books = [follows.book for follows in db_followed]
    return db_books    

@router.get("{user_id}/owned")
def get_owned_books_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_owned = db.query(models.Ownership).filter(models.Ownership.user_id == user_id).all()
    if db_owned is None:
        raise HTTPException(status_code=404, detail="Owned books or user not found")
    
    # should i query this way or just take books from onwer relation
    #db_books = db.query(models.Book).filter(models.Book.id in db_owned[0].book_id)
    db_books = [ownership.book for ownership in db_owned]
    return db_books
