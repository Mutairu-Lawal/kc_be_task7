from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models import Contact, User
from database import get_session
from lib import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter(tags=['contacts'])


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = session.exec(select(User).where(
        User.username == payload.get("sub"))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("/contacts/", response_model=Contact)
def create_contact(contact: Contact, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    contact.user_id = user.id
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


@router.get("/contacts/", response_model=List[Contact])
def get_contacts(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    contacts = session.exec(select(Contact).where(
        Contact.user_id == user.id)).all()
    return contacts


@router.put("/contacts/{id}", response_model=Contact)
def update_contact(id: int, contact: Contact, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    db_contact = session.get(Contact, id)
    if not db_contact or db_contact.user_id != user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    db_contact.name = contact.name
    db_contact.email = contact.email
    db_contact.phone = contact.phone
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact


@router.delete("/contacts/{id}")
def delete_contact(id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    db_contact = session.get(Contact, id)
    if not db_contact or db_contact.user_id != user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    session.delete(db_contact)
    session.commit()
    return {"ok": True}
