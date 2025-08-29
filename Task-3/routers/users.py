from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import Users
from lib import *


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=201)
def create_user(data: Users, users=Depends(load_users)):
    post_data = data.model_dump()
    for user in users:
        if user.get('username', '').lower() == post_data['username'].lower():
            raise HTTPException(
                status_code=400, detail='username already exists')

    hashed_password = password_hashed(post_data['password'])

    # Assign unique id
    max_id = max([user.get('id', 0) for user in users], default=0)
    new_id = max_id + 1
    post_data.update({
        "password": hashed_password,
        "id": new_id
    })
    save_users(post_data, users)
    return {"data": post_data['username'], "id": new_id}


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
