from fastapi import FastAPI
from fastapi import FastAPI, Request, Response
import time
from database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from routers import products, cart, admin, users
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db_and_tables()
    yield
    # Shutdown code (if any)

app = FastAPI(title="E-Commerce API", lifespan=lifespan)


# Middleware to measure response time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # ms
    response.headers["X-Process-Time"] = str(round(process_time, 2))
    return response


# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(users.router, prefix="/user", tags=["users"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
