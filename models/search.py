from pydantic import BaseModel, Field
from models.topics import ContentType


class SearchParamsFilter(BaseModel):
    query: str
    content: list[str]
    topics: list[str]

class SearchResults(BaseModel):
    avul: ContentType = ContentType()
    cri: ContentType = ContentType()
    dawm: ContentType = ContentType()
    sysop: ContentType = ContentType()
    scomp: ContentType = ContentType()
    ia: ContentType = ContentType()

