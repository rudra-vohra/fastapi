from fastapi import APIRouter, Depends, HTTPException,Query
from auth import verify_api_key
from models.books import Book, CreateBook, ReadBook, UpdateBook
from sqlmodel import Session, select
from typing import Optional
from database import get_session


router = APIRouter(prefix='/books',tags=['books'])

@router.get('/',response_model=list[ReadBook])
def get_books(
    title: Optional[str]  = Query(default=None,description='Filter books by title'),
    author: Optional[str]  = Query(default=None,description='Filter books by author'),
    session:Session = Depends(get_session)
):
    query = select(Book).where(
        Book.is_sold == False
    )

    if title:
        query = query.where(Book.title == title)
    if author:
        query = query.where(Book.author == author)

    books = session.exec(query).all()
    return books

@router.post('/',response_model=ReadBook)
def create_book(
    book_data : CreateBook,
    session : Session = Depends(get_session),
    api_key : str = Depends(verify_api_key)
):
    book = Book.model_validate(book_data)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.patch('/{book_id}',response_model=ReadBook)
def update_book(
    book_id: int,
    book_data : UpdateBook,
    session : Session = Depends(get_session),
    api_key : str = Depends(verify_api_key)
):
    book = select(Book,book_id)
    if not book:
        raise HTTPException(status_code=404,detail='Book not found')

    
    book_update = book_data.model_dump(exclude_unset=True)

    for key, value in book_update.items():
        setattr(book,key,value)

    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.patch('/{book_id}/sold',response_model=ReadBook)
def sold_book(
    book_id: int,
    session : Session = Depends(get_session),
    api_key : str = Depends(verify_api_key)
):
    book = select(Book,book_id)
    if not book:
        raise HTTPException(status_code=404,detail='Book not found')
    
    book.is_sold = True

    session.add(book)
    session.commit()
    session.refresh(book)
    return book







