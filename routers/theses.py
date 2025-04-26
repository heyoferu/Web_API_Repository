from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from db import get_session, Session
from models.theses import Theses, ThesesFilterParams
from typing import Annotated
from rapidfuzz import process

# security_scheme = HTTPBearer()

router = APIRouter(tags=['Theses'])

@router.get('/theses')
async def get_theses(filters: Annotated[ThesesFilterParams, Query()], session: Session = Depends(get_session)):
    if filters.limit:
        statement = select(Theses).limit(filters.limit)
    else:
        statement = select(Theses)
        
    # if filters.tags:
    #     statement.where(Theses.tags in filters.tags)
    

    theses = session.exec(statement).all()

    if not theses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Theses not found'
        )

    
    if filters.title:
        theses = [thesis for thesis in theses if process.extract(thesis.title.lower(),[filters.title.lower()],score_cutoff=90)]

    return theses


@router.post('/theses')
async def create_theses(new_thesis: Theses, session: Session = Depends(get_session)):
    try:
        session.add(new_thesis)
        session.commit()
        return status.HTTP_201_CREATED
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Thesis not created'
        )
    finally:
        session.close()

@router.put('/theses')
async def update_theses(id: int, new_data: Theses, session: Session = Depends(get_session)):
    statement = select(Theses).where(Theses.id == id)
    thesis = session.exec(statement).one_or_none()

    if not thesis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Thesis not found'
        )

    session.add(new_data)
    session.commit()
    session.close()

    return status.HTTP_200_OK
@router.delete('/theses')
async def delele_theses(id: int, session: Session = Depends(get_session)):

    statement = select(Theses).where(Theses.id == id)
    thesis_to_delete = session.exec(statement).one_or_none()

    if not thesis_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Thesis not found'
        )
    
    session.delete(thesis_to_delete)
    session.commit()
    session.close()

    return status.HTTP_200_OK