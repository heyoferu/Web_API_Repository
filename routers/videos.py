from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from db import get_session, Session
from models.videos import Videos, VideosFilterParams
from typing import Annotated
from rapidfuzz import process

# security_scheme = HTTPBearer()

router = APIRouter(tags=['Videos'])

@router.get('/videos')
async def get_videos(filters: Annotated[VideosFilterParams, Query()], session: Session = Depends(get_session)):
    if filters.limit:
        statement = select(Videos).limit(filters.limit)
    else:
        statement = select(Videos)

    #     statement.where(Videos.tags in filters.tags)
    

    videos = session.exec(statement).all()

    if not videos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Videos not found'
        )

    
    if filters.title:
        videos = [video for video in videos if process.extract(video.title.lower(),[filters.title.lower()],score_cutoff=90)]

    return videos


@router.post('/videos')
async def create_videos(new_video: Videos, session: Session = Depends(get_session)):
    try:
        session.add(new_video)
        session.commit()
        return status.HTTP_201_CREATED
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Video not created'
        )
    finally:
        session.close()

@router.put('/videos')
async def update_videos(id: int, new_data: Videos, session: Session = Depends(get_session)):
    statement = select(Videos).where(Videos.id == id)
    video = session.exec(statement).one_or_none()

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Video not found'
        )

    session.add(new_data)
    session.commit()
    session.close()

    return status.HTTP_200_OK
@router.delete('/videos')
async def delele_videos(id: int, session: Session = Depends(get_session)):

    statement = select(Videos).where(Videos.id == id)
    video_to_delete = session.exec(statement).one_or_none()

    if not video_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Video not found'
        )
    
    session.delete(video_to_delete)
    session.commit()
    session.close()

    return status.HTTP_200_OK