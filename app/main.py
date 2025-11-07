from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import article
from app.core.db import

app = FastAPI()

def on_startup():
    create_db_and_tables()
app.include_router(article.router)