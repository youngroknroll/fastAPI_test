from fastapi import FastAPI

from app.api import article

app = FastAPI()

app.include_router(article.router)