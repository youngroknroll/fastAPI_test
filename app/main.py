from fastapi import FastAPI

from app.api import article
from app.core.db import init_db

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(article.router)