from fastapi import APIRouter, Depends, HTTPException
from models import Users
from lib import load_users, password_hashed, save_users


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


# @router.post("/login")
# def login_user():
#     return {"message": "User logged in successfully"}
