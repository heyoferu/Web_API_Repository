from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from db import get_session, Session
from models.books import Books, BooksFilterParams
from typing import Annotated
from rapidfuzz import process

# security_scheme = HTTPBearer()

router = APIRouter(tags=['Books'])

@router.get('/books')
async def get_books(filters: Annotated[BooksFilterParams, Query()], session: Session = Depends(get_session)):
    if filters.limit:
        statement = select(Books).limit(filters.limit)
    else:
        statement = select(Books)

    if filters.isbn:
        statement.where(Books.isbn == filters.isbn)
    # if filters.tags:
    #     statement.where(Books.tags in filters.tags)
    

    books = session.exec(statement).all()

    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Books not found'
        )

    
    if filters.title:
        books = [book for book in books if process.extract(book.title.lower(),[filters.title.lower()],score_cutoff=90)]

    return books


@router.post('/books')
async def create_books(new_book: Books, session: Session = Depends(get_session)):
    try:
        session.add(new_book)
        session.commit()
        return status.HTTP_201_CREATED
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Book not created'
        )
    finally:
        session.close()

@router.put('/books')
async def update_books(id: int, new_data: Books, session: Session = Depends(get_session)):
    statement = select(Books).where(Books.id == id)
    book = session.exec(statement).one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )

    session.add(new_data)
    session.commit()
    session.close()

    return status.HTTP_200_OK
@router.delete('/books')
async def delele_books(id: int, session: Session = Depends(get_session)):

    statement = select(Books).where(Books.id == id)
    book_to_delete = session.exec(statement).one_or_none()

    if not book_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    
    session.delete(book_to_delete)
    session.commit()
    session.close()

    return status.HTTP_200_OK