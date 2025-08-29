from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.notes import router as notes_router
from contextlib import asynccontextmanager
from database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db_and_tables()
    yield
    # Shutdown code (if any)

app = FastAPI(title="Note API", lifespan=lifespan)


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

request_count = 0


@app.middleware("http")
async def count_requests(request: Request, call_next):
    global request_count
    request_count += 1
    response = await call_next(request)
    print(f"Total requests: {request_count}")
    return response

app.include_router(notes_router, prefix="/notes", tags=["notes"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
