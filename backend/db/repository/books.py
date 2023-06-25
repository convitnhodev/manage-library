from sqlalchemy.orm import Session

from schemas.books import BookModel
from schemas.books import DetailAddingBook
from schemas.helper import CustomJSONEncoder
from db.models.books import Book
import json
import uuid



def add_book(book: DetailAddingBook, db: Session):
    existing_book = db.query(Book).filter(
        Book.owner == book.owner,
        Book.book_name == book.book_name,
        Book.category == book.category,
        Book.author == book.author,
        Book.year_of_publication == book.year_of_publication
    ).first()

    if existing_book:
        # Update the existing book's numbers
        existing_book.numbers += book.numbers
        db.commit()
        db.refresh(existing_book)
        return existing_book


    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def list_books_by_owner(owner: str, db: Session, offset: int , limit: int):
    books = db.query(Book).filter(Book.owner == owner).offset(offset).limit(limit).all()
    return books


def get_book_by_id(id: int,owner: str, db: Session):
    book = db.query(Book).filter(Book.id == id, Book.owner == owner).first()
    return book


def delete_book_by_id(id: int, owner: str, db: Session) -> Book:
    book = db.query(Book).filter(Book.id == id, Book.owner == owner).first()
    
    if book:
        db.delete(book)
        db.commit()
        return book

    return None

