from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api import article
from app.core.db import init_db

def start():
    print("Starting server...")
    init_db()

def shutdown():
    print("Shutting down server...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    start()
    yield
    shutdown()

app = FastAPI(lifespan=lifespan)
app.include_router(article.router)  
