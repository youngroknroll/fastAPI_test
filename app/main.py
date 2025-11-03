from fastapi import FastAPI
from app.api.routers import article_router
app = FastAPI()

app.include_router(article_router.router, prefix="/articles", tags=["articles"])
