from datetime import date
from sqlmodel import Field, SQLModel

class Users(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    lname: str
    email: str
    password: str

class UserCredentials(SQLModel):
    email: str
    password: str

class UserUpdate(SQLModel):
    id: str
    email: str
    name: str
    lname: str    

class UserNewCredentials(SQLModel):
    id: str
    oldpassword: str
    newpassword: str
    confirmpassword: str

class Books(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    author: str
    editorial: str
    isbn: str
    pages: str
    date: date
    path: str

class Magazines(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    editorial: str
    issn: str
    volume: str
    number: str
    date: date
    path: str 

class Podcasts(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    host: str
    episode: int
    duration: int 
    date: date
    path: str

class Tesis(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    author: str
    school: str
    grade: str  # Licenciatura, Maestría, Doctorado
    principal: str
    date: date
    path: str 

class Videos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    creator: str
    duration: int
    date: date
    path: str  # Ruta del archivo de video
