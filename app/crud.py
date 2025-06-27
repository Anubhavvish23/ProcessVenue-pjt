from sqlalchemy.orm import Session
from app import models, schemas


# --- BOOK CRUD ---

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# --- REVIEW CRUD ---

def create_review(db: Session, review: schemas.ReviewCreate, book_id: int):
    db_review = models.Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews_by_book(db: Session, book_id: int):
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()
