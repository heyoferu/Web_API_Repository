from pydantic import BaseModel

from models.books import Books
from models.magazines import Magazines
from models.podcasts import Podcasts
from models.theses import Theses
from models.videos import Videos


class ContentType(BaseModel):
    books: list[Books] = []
    magazines: list[Magazines] = []
    theses: list[Theses] = []
    podcasts: list[Podcasts] = []
    videos: list[Videos] = []