from datetime import date
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Column, Field, SQLModel, ARRAY, String

class Podcasts(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    host: str
    episode: int
    duration: int 
    date: date
    path: str
    code: str
    tags: list[str] = Field(default=[], sa_column=Column(ARRAY(String)))

class PodcastsFilterParams(BaseModel):
    model_config = {'extra':'forbid'}
    title: Optional[str] = None
    limit: Optional[int] = Field(None, gt=0)
    tags: list[str] = []
