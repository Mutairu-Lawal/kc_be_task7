from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import List, Optional
import json
import os
from datetime import datetime, timedelta, timezone
from models import UserInFile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

USERS_FILE = 'users.json'
SECRET_KEY = 'kodecamp-final-task-to-capstone-project'
ALGORITHM = "HS256"


def authenticate_user(username: str, password: str) -> bool:
    users = load_users()
    for u in users:
        if u.username == username and pwd_context.verify(password, u.hashed_password):
            return True
    return False


def password_hashed(PLAIN_PASSWORD):
    return pwd_context.hash(PLAIN_PASSWORD)


def load_users(path: str = USERS_FILE) -> List[UserInFile]:
    if not os.path.exists(USERS_FILE):
        return []
    with open(path, "r") as f:
        raw = json.load(f)
    return [UserInFile(**r) for r in raw]


def save_users(data: UserInFile, users: List[UserInFile]):
    users.append(UserInFile(**data))
    with open(USERS_FILE, "w") as f:
        json.dump([u.dict() for u in users], f, indent=4)


# def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise HTTPException(
#                 status_code=404, detail="incorrect username or password")
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
