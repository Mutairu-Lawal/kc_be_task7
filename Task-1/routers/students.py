from fastapi import APIRouter, Depends, HTTPException, status
from models import StudentCreate, StudentRead, Student, UserInFile
from fastapi.security import OAuth2PasswordRequestForm
from lib import *
from datetime import timedelta
from database import get_session
from sqlmodel import Session, select
from typing import Annotated


ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.post('/create-student', status_code=201)
def create_user(data: UserInFile, users=Depends(load_users)):
    post_data = data.model_dump()
    for user in users:
        if user.username.lower() == post_data['username'].lower():
            raise HTTPException(
                status_code=400, detail='username already exists')

    hashed_password = password_hashed(post_data['hashed_password'])

    post_data.update({
        "hashed_password": hashed_password
    })
    save_users(post_data, users)
    return {"msg": "User created successfully"}


# private route
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if not authenticate_user(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/')
def get_students(session: Session = Depends(get_session),
                 offset: int = 0, limit: int = 10):
    students = session.exec(select(Student).offset(offset).limit(limit)).all()
    return students


@router.put("/{student_id}", response_model=StudentRead, status_code=status.HTTP_202_ACCEPTED)
def create_student(student_id: int, student_data: StudentCreate, session: Session = Depends(get_session), username=Depends(get_current_user)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    student.name = student_data.name
    student.age = student_data.age
    student.grades = student_data.grades
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, session: Session = Depends(get_session), username=Depends
                   (get_current_user)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"msg": "Student deleted successfully"}


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, session: Session = Depends(get_session), username=Depends
                (get_current_user)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student
