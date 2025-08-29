from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False)


class NoteCreate(SQLModel):
    title: str
    content: str


class NoteRead(SQLModel):
    id: int
    title: str
    content: str
    created_at: datetime
