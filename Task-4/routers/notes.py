from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from models import Note, NoteCreate, NoteRead
from database import get_session
import json

router = APIRouter()

NOTES_JSON = "notes.json"


def backup_notes():
    with get_session() as session:
        notes = session.exec(select(Note)).all()
        with open(NOTES_JSON, "w", encoding="utf-8") as f:
            json.dump([note.dict()
                      for note in notes], f, default=str, indent=2)


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(note: NoteCreate, session=Depends(get_session)):
    db_note = Note(**note.model_dump())
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    backup_notes()
    return db_note


@router.get("/", response_model=list[NoteRead])
def list_notes(session=Depends(get_session)):
    notes = session.exec(select(Note)).all()
    return notes


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, session=Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}")
def delete_note(note_id: int, session=Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    backup_notes()
    return {"detail": "Note deleted"}
