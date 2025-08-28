from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr, BaseModel


# ---------- DB models ----------
class StudentBase(SQLModel):
    name: str
    age: int = Field(gt=1)
    email: EmailStr
    # We'll store grades as a JSON string in SQLite; for other DBs, you can use JSON type
    grades: Optional[str] = "[]"


class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int


class StudentUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    grades: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInFile(BaseModel):
    username: str
    hashed_password: str
