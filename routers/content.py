from fastapi import APIRouter, Depends
from sqlmodel import select
from db import get_session, Session
from models import Books, Magazines, Podcasts, Tesis, Videos
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


#scheme = HTTPBearer()
# token: str = Depends(scheme)

router = APIRouter(prefix="/content", tags=["content"])

# CRUD CONTENT
# ------- books routes 
@router.get("/books")
async def get_books(session: Session = Depends(get_session)):
    statement = select(Books)
    query_get_books = session.exec(statement)
    if query_get_books:
        return query_get_books.all()
    else:
        return False
    
@router.post("/books")
async def create_books(new_book: Books, session: Session = Depends(get_session)):
    try:
        session.add(new_book)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

@router.put("/books")
async def update_books(book_new_data: Books, session: Session = Depends(get_session)):
    statement = select(Books).where(Books.id == book_new_data.id)
    book_to_update = session.exec(statement).one()
    book_to_update.author = book_new_data.author
    book_to_update.title = book_new_data.title
    book_to_update.editorial = book_new_data.editorial
    book_to_update.isbn = book_new_data.isbn
    book_to_update.pages= book_new_data.pages
    book_to_update.date = book_new_data.date
    book_to_update.path = book_new_data.path

    try:
        session.add(book_to_update)
        session.commit()
        return True
    
    except Exception as e:
        print(e)
        session.rollback()
        return False
    finally:
        session.close()

@router.delete('/books/{id}')
async def delete_books(id: int, session: Session = Depends(get_session)):
    try:
        statement = select(Books).where(Books.id == id)
        book_to_delete = session.exec(statement).one()
        if book_to_delete:
            session.delete(book_to_delete)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        return False
    
    finally:
        session.close()

    
# -------magazines routes
@router.get("/magazines")
async def get_magazines(session: Session = Depends(get_session)):
    statement = select(Magazines)
    query_get_magazines = session.exec(statement)
    if query_get_magazines:
        return query_get_magazines.all()
    else:
        return False
    
@router.post("/magazines")
async def create_magazines(new_magazine: Magazines, session: Session = Depends(get_session)):
    try:
        session.add(new_magazine)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()   

@router.put("/magazines")
async def update_magazines(magazine_new_data: Magazines, session: Session = Depends(get_session)):
    statement = select(Magazines).where(Magazines.id == magazine_new_data.id)
    magazine_to_update = session.exec(statement).one()

    magazine_to_update.title = magazine_new_data.title
    magazine_to_update.editorial = magazine_new_data.editorial
    magazine_to_update.issn = magazine_new_data.issn
    magazine_to_update.volume = magazine_new_data.volume
    magazine_to_update.number= magazine_new_data.number
    magazine_to_update.date = magazine_new_data.date
    magazine_to_update.path = magazine_new_data.path

    try:
        session.add(magazine_to_update)
        session.commit()
        return True
    
    except Exception as e:
        print(e)
        session.rollback()
        return False
    finally:
        session.close()

@router.delete('/magazines/{id}')
async def delete_magazines(id: int, session: Session = Depends(get_session)):
    try:
        statement = select(Magazines).where(Magazines.id == id)
        magazine_to_delete = session.exec(statement).one()
        if magazine_to_delete:
            session.delete(magazine_to_delete)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        return False
    
    finally:
        session.close()

# -------podcasts routes
@router.get("/podcasts")
async def get_podcasts(session: Session = Depends(get_session)):
    statement = select(Podcasts)
    query_get_podcasts = session.exec(statement)
    if query_get_podcasts:
        return query_get_podcasts.all()
    else:
        return False
    
@router.post("/podcasts")
async def create_podcasts(new_podcast: Podcasts, session: Session = Depends(get_session)):
    try:
        session.add(new_podcast)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()


@router.put("/podcast")
async def update_podcast(podcast_new_data: Podcasts, session: Session = Depends(get_session)):
    statement = select(Podcasts).where(Podcasts.id == podcast_new_data.id)
    podcast_to_update = session.exec(statement).one()

    podcast_to_update.title = podcast_new_data.title
    podcast_to_update.editorial = podcast_new_data.editorial
    podcast_to_update.issn = podcast_new_data.issn
    podcast_to_update.volume = podcast_new_data.volume
    podcast_to_update.number= podcast_new_data.number
    podcast_to_update.date = podcast_new_data.date
    podcast_to_update.path = podcast_new_data.path

    try:
        session.add(podcast_to_update)
        session.commit()
        return True
    
    except Exception as e:
        print(e)
        session.rollback()
        return False
    finally:
        session.close()

@router.delete('/podcast/{id}')
async def delete_podcasts(id: int, session: Session = Depends(get_session)):
    try:
        statement = select(Podcasts).where(Podcasts.id == id)
        podcasts_to_delete = session.exec(statement).one()
        if podcasts_to_delete:
            session.delete(podcasts_to_delete)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        return False
    
    finally:
        session.close()

# -------tesis routes
@router.get("/tesis")
async def get_tesis(session: Session = Depends(get_session)):
    statement = select(Tesis)
    query_get_tesis = session.exec(statement)
    if query_get_tesis:
        return query_get_tesis.all()
    else:
        return False
    
@router.post("/tesis")
async def create_tesis(new_tesis: Tesis, session: Session = Depends(get_session)):
    try:
        session.add(new_tesis)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()  


@router.put("/tesis")
async def update_tesis(tesis_new_data: Tesis, session: Session = Depends(get_session)):
    statement = select(Tesis).where(Tesis.id == tesis_new_data.id)
    tesis_to_update = session.exec(statement).one()

    tesis_to_update.title = tesis_new_data.title
    tesis_to_update.author = tesis_new_data.author
    tesis_to_update.school = tesis_new_data.school
    tesis_to_update.grade= tesis_new_data.grade
    tesis_to_update.principal = tesis_new_data.principal
    tesis_to_update.date = tesis_new_data.date
    tesis_to_update.path = tesis_new_data.path

    try:
        session.add(tesis_to_update)
        session.commit()
        return True
    
    except Exception as e:
        print(e)
        session.rollback()
        return False
    finally:
        session.close()

@router.delete('/tesis/{id}')
async def delete_tesis(id: int, session: Session = Depends(get_session)):
    try:
        statement = select(Tesis).where(Tesis.id == id)
        tesis_to_delete = session.exec(statement).one()
        if tesis_to_delete:
            session.delete(tesis_to_delete)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        return False
    
    finally:
        session.close()


# -------videos routes
@router.get("/videos")
async def get_videos(session: Session = Depends(get_session)):
    statement = select(Videos)
    query_get_videos = session.exec(statement)
    if query_get_videos:
        return query_get_videos.all()
    else:
        return False
    
@router.post("/videos")
async def create_videos(new_video: Videos, session: Session = Depends(get_session)):
    try:
        session.add(new_video)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()


@router.put("/videos")
async def update_videos(video_new_data: Videos, session: Session = Depends(get_session)):
    statement = select(Videos).where(Videos.id == video_new_data.id)
    videos_to_update = session.exec(statement).one()

    videos_to_update.title = video_new_data.title
    videos_to_update.creator = video_new_data.creator
    videos_to_update.duration = video_new_data.duration
    videos_to_update.date = video_new_data.date
    videos_to_update.path = video_new_data.path

    try:
        session.add(videos_to_update)
        session.commit()
        return True
    
    except Exception as e:
        print(e)
        session.rollback()
        return False
    finally:
        session.close()

@router.delete('/videos/{id}')
async def delete_videos(id: int, session: Session = Depends(get_session)):
    try:
        statement = select(Videos).where(Videos.id == id)
        video_to_delete = session.exec(statement).one()
        if video_to_delete:
            session.delete(video_to_delete)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        return False
    
    finally:
        session.close()