from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import BaseModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    contacts: List["Contact"] = Relationship(back_populates="user")


class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="contacts")


class Users(BaseModel):
    username: str
    password: str
