from typing import Optional
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from typing import List
import json
import os
from datetime import datetime, timedelta, timezone
from models import UserInFile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="students/login")

USERS_FILE = 'users.json'
SECRET_KEY = 'kodecamp-final-task-to-capstone-project'
ALGORITHM = "HS256"


def authenticate_user(username: str, password: str) -> Optional[UserInFile]:
    users = load_users()
    for u in users:
        if u.username.lower() == username.lower() and pwd_context.verify(password, u.hashed_password):
            return True
    return None


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


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    # users = load_users()
    # user = next((u for u in users if u["username"] == username), None)
    # if not user:
    #     raise HTTPException(status_code=401, detail="User not found")
    # return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
