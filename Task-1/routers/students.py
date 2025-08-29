from fastapi import APIRouter, Depends, HTTPException, status
from models import StudentCreate, StudentRead, Student, UserInFile
from fastapi.security import OAuth2PasswordRequestForm
from lib import *
from datetime import timedelta
from database import get_session
from sqlmodel import Session
from typing import Annotated


ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.get('/')
def home(users=Depends(load_users)):
    return {'data': users}


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


@router.post("/login",)
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


@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentCreate, session: Session = Depends(get_session), username=Depends(get_current_user)):
    student = Student(name=student_data.name, age=student_data.age,
                      email=student_data.email, grades=student_data.grades)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student
