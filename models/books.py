from datetime import date
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Column, Field, SQLModel, ARRAY, String


class Books(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    author: str
    editorial: str
    isbn: str
    pages: str
    date: date
    path: str
    code: str
    tags: list[str] = Field(default=[], sa_column=Column(ARRAY(String)))


class BooksFilterParams(BaseModel):
    model_config = {'extra':'forbid'}
    isbn: Optional[str] = None
    title: Optional[str] = None
    limit: Optional[int] = Field(None, gt=0)
    tags: list[str] = []

