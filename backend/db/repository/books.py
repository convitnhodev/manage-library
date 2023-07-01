from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.books import BookModel
from schemas.books import DetailAddingBook
from schemas.helper import CustomJSONEncoder
from db.models.books import Book
import json
import uuid
from typing import List
from datetime import date, datetime



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


def list_books_borred_by_owner(owner: str, db: Session, offset: int, limit: int):
    books = db.query(Book).filter(Book.owner == owner, Book.amount_borrowed > 0).offset(offset).limit(limit).all()
    total_records = db.query(func.count(Book.id)).filter(Book.owner == owner).scalar()
    return books, total_records

def get_book_by_id(id: int,owner: str, db: Session):
    book = db.query(Book).filter(Book.id == id, Book.owner == owner).first()
    return book

# adding 
def get_books_by_ids(ids: List[int], owner: str, db: Session):
    books = db.query(Book).filter(Book.id.in_(ids), Book.owner == owner).all()
    return books 


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
    existing_book.amount_borrowed = book.amount_borrowed

    db.commit()
    db.refresh(existing_book)
    return existing_book


def update_book_amount_borrowed(id: int, amount: int, owner: str, db: Session): 
    book = db.query(Book).filter(Book.id == id, Book.owner == owner).first()
    book.amount_borrowed = book.amount_borrowed + amount
    db.commit()
    db.refresh(book)
    return book


def update_books_amount_borrowed(ids: List[int], amount: int, owner: str, db: Session, date_return: date, date_must_return: date, is_return: bool): 
    
    if not isinstance(ids, list):
        ids = [ids]  # Wrap single v
    books = db.query(Book).filter(Book.id.in_(ids), Book.owner == owner).all()
    
    
    for book in books:
        book.amount_borrowed += amount
        book.date_return = date_return
        book.date_must_return = date_must_return
        book.date_borrowed = datetime.now()
        book.is_return = is_return

    db.commit()
    
    return books


def list_book_borrow(owner: str, db: Session): 
    books = db.query(Book).filter(Book.owner == owner, Book.is_return == False).all()
    return books 
