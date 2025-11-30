"""FastAPI Application Entry Point"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import auth
from app.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (cleanup if needed)


app = FastAPI(title="RealWorld API", version="0.1.0", lifespan=lifespan)

app.include_router(auth.router)


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

