from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers.contacts import router as contacts_router
from lib import get_password_hash, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from models import User, Users
from database import get_session
from sqlmodel import Session, select
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db_and_tables()
    yield
    # Shutdown code (if any)

app = FastAPI(title="Contact Manager API", lifespan=lifespan)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to log IP address
@app.middleware("http")
async def log_ip(request: Request, call_next):
    ip = request.client.host
    print(f"Request from IP: {ip}")
    response = await call_next(request)
    return response


app.include_router(contacts_router)


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(
        User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
def register(form_data: Users, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(
        User.username == form_data.username)).first()
    if user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(form_data.password)
    new_user = User(username=form_data.username,
                    hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"msg": "User registered successfully"}
