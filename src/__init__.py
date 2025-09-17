from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting ...")
    await init_db() #It is a call routine function so it has to always be called with await.
    yield
    print(f"server has been stopped")

version = "v1"

app = FastAPI(
    title="Bookly",
    version=version,
    description="A REST API for a book review web service",
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])