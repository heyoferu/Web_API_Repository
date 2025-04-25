from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from db import get_session, Session
from models.podcasts import Podcasts, PodcastsFilterParams
from typing import Annotated
from rapidfuzz import process

# security_scheme = HTTPBearer()

router = APIRouter(tags=['Podcasts'])

@router.get('/podcasts')
async def get_podcasts(filters: Annotated[PodcastsFilterParams, Query()], session: Session = Depends(get_session)):
    if filters.limit:
        statement = select(Podcasts).limit(filters.limit)
    else:
        statement = select(Podcasts)

    if filters.isbn:
        statement.where(Podcasts.isbn == filters.isbn)
    # if filters.tags:
    #     statement.where(Podcasts.tags in filters.tags)
    

    podcasts = session.exec(statement).all()

    if not podcasts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Podcasts not found'
        )

    
    if filters.title:
        podcasts = [podcast for podcast in podcasts if process.extract(podcast.title.lower(),[filters.title.lower()],score_cutoff=90)]

    return podcasts


@router.post('/podcasts')
async def create_podcasts(new_podcast: Podcasts, session: Session = Depends(get_session)):
    try:
        session.add(new_podcast)
        session.commit()
        return status.HTTP_201_CREATED
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Podcast not created'
        )
    finally:
        session.close()

@router.put('/podcasts')
async def update_podcasts(id: int, new_data: Podcasts, session: Session = Depends(get_session)):
    statement = select(Podcasts).where(Podcasts.id == id)
    podcast = session.exec(statement).one_or_none()

    if not podcast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Podcast not found'
        )

    session.add(new_data)
    session.commit()
    session.close()

    return status.HTTP_200_OK
@router.delete('/podcasts')
async def delele_podcasts(id: int, session: Session = Depends(get_session)):

    statement = select(Podcasts).where(Podcasts.id == id)
    podcast_to_delete = session.exec(statement).one_or_none()

    if not podcast_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Podcast not found'
        )
    
    session.delete(podcast_to_delete)
    session.commit()
    session.close()

    return status.HTTP_200_OK