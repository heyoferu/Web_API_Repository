from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from db import get_session, Session
from models.magazines import Magazines, MagazinesFilterParams
from typing import Annotated
from rapidfuzz import process

# security_scheme = HTTPBearer()

router = APIRouter(tags=['Magazines'])

@router.get('/magazines')
async def get_magazines(filters: Annotated[MagazinesFilterParams, Query()], session: Session = Depends(get_session)):
    if filters.limit:
        statement = select(Magazines).limit(filters.limit)
    else:
        statement = select(Magazines)

    if filters.issn:
        statement.where(Magazines.issn == filters.issn)
    # if filters.tags:
    #     statement.where(Magazines.tags in filters.tags)
    

    magazines = session.exec(statement).all()

    if not magazines:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Magazines not found'
        )

    
    if filters.title:
        magazines = [magazine for magazine in magazines if process.extract(magazine.title.lower(),[filters.title.lower()],score_cutoff=90)]

    return magazines


@router.post('/magazines')
async def create_magazines(new_magazine: Magazines, session: Session = Depends(get_session)):
    try:
        session.add(new_magazine)
        session.commit()
        return status.HTTP_201_CREATED
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Magazine not created'
        )
    finally:
        session.close()

@router.put('/magazines')
async def update_magazines(id: int, new_data: Magazines, session: Session = Depends(get_session)):
    statement = select(Magazines).where(Magazines.id == id)
    magazine = session.exec(statement).one_or_none()

    if not magazine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Magazine not found'
        )

    session.add(new_data)
    session.commit()
    session.close()

    return status.HTTP_200_OK
@router.delete('/magazines')
async def delele_magazines(id: int, session: Session = Depends(get_session)):

    statement = select(Magazines).where(Magazines.id == id)
    magazine_to_delete = session.exec(statement).one_or_none()

    if not magazine_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Magazine not found'
        )
    
    session.delete(magazine_to_delete)
    session.commit()
    session.close()

    return status.HTTP_200_OK