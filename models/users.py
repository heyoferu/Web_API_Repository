from datetime import date
from typing import Optional
from pydantic import BaseModel
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

class UserInfo(SQLModel):
    id: str
    email: str
    name: str
    lname: str    

class UserNewCredentials(SQLModel):
    id: str
    oldpassword: str
    newpassword: str
    confirmpassword: str

