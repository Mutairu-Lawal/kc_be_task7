from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import Users
from lib import *


router = APIRouter()


@router.post("/register")
def create_user(data: Users, users=Depends(load_users)):
    post_data = data.model_dump()
    for user in users:
        if user.username.lower() == post_data['username'].lower():
            raise HTTPException(
                status_code=400, detail='username already exists')

    if post_data['role'] not in ['admin', 'user']:
        raise HTTPException(
            status_code=400, detail='Invalid role')

    hashed_password = password_hashed(post_data['password'])

    post_data.update({
        "password": hashed_password
    })
    save_users(post_data, users)
    return {"msg": "User created successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if not authenticate_user(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=60)

    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
