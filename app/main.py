"""FastAPI Application Entry Point"""

from fastapi import FastAPI

from app.api import auth

app = FastAPI(title="RealWorld API", version="0.1.0")

app.include_router(auth.router)


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

