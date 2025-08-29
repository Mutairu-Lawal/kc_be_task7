from fastapi import FastAPI, Request, HTTPException
from routers.applications import router as applications_router
from routers.users import router as users_router
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db_and_tables()
    yield
    # Shutdown code (if any)

app = FastAPI(title="Job Apllication Tracker", lifespan=lifespan)


# Middleware to reject requests missing User-Agent header
class UserAgentMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if 'user-agent' not in request.headers:
            raise HTTPException(
                status_code=400, detail="User-Agent header required")
        return await call_next(request)


app.add_middleware(UserAgentMiddleware)


# Routers
app.include_router(applications_router)
app.include_router(users_router)
