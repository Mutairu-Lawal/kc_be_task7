from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from pydantic import BaseModel


class JobPost(SQLModel):
    company: str
    position: str
    status: str
    date_applied: date


class JobApplication(JobPost, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class Users(BaseModel):
    username: str
    password: str


class UsersCreated(Users):
    id: int
