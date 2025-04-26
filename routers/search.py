from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlmodel import select
from db import get_session, Session
from rapidfuzz import process
from models.books import Books
from models.magazines import Magazines
from models.search import SearchParamsFilter, SearchResults
from models.theses import Theses
from models.podcasts import Podcasts
from models.videos import Videos

router = APIRouter(tags=['Search'])

@router.get('/search')
async def search(search_params: Annotated[SearchParamsFilter, Query()], session: Session = Depends(get_session)):

    search_result = SearchResults()

    ALLOWED_CONTENT = {
        "books" : Books,
        "magazines" : Magazines,
        "theses" : Theses,
        "podcasts" : Podcasts,
        "videos" : Videos
    }

    for topic in search_params.topics:
        for content_key in search_params.content:
            model = ALLOWED_CONTENT[content_key]
            result = session.exec(select(model).where(model.code == topic)).all()
            result = [item for item in result if process.extract(item.title.lower(),[search_params.query.lower()],score_cutoff=90)]

            if hasattr(search_result, topic):
                setattr(getattr(search_result, topic), content_key, result)
    
    return search_result
