from fastapi import FastAPI
from database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from routers import students
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db_and_tables()
    yield
    # Shutdown code (if any)

app = FastAPI(title="Student Management API", lifespan=lifespan)


# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(students.router, prefix="/students", tags=["students"])
