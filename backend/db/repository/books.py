from sqlalchemy.orm import Session
from sqlalchemy import func
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

def list_books_by_owner(owner: str, db: Session, offset: int, limit: int):
    books = db.query(Book).filter(Book.owner == owner).offset(offset).limit(limit).all()
    total_records = db.query(func.count(Book.id)).filter(Book.owner == owner).scalar()
    return books, total_records

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


def update_book_by_id(book: DetailAddingBook, db:Session, id: int, updated_by: str):
    existing_book = db.query(Book).filter(Book.owner == book.owner, Book.id == id).first()
    if existing_book is None: 
        return None
    
    existing_book.book_name = book.book_name
    existing_book.category = book.category
    existing_book.author = book.author
    existing_book.year_of_publication = book.year_of_publication
    existing_book.publisher = book.publisher
    existing_book.updated_by = updated_by
    existing_book.numbers = book.numbers

    db.commit()
    db.refresh(existing_book)
    return existing_book



