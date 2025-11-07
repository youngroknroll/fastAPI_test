from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.repositories.article_repo import ArticleRepo
from app.schemas.article_schema import ArticleCreate, ArticleResponse


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/")
def list_articles():
    return articles

@router.get("/{id}")
def get_article(id: int):
    for article in articles:
        if article["id"] == id:
            return article
    raise HTTPException(status_code=404, detail="article not found")

@router.post("/")
def create_article(article: Article):
    new_id = max(a["id"] for a in articles) + 1 if articles else 1
    new_article = {"id": new_id, "title": article.title, "author": article.author}
    articles.append(new_article)
    return new_article

@router.put("/{id}")
def update_article(id: int, article: Article):
    for article in articles:
        if article["id"] == id:
            article.title = article.title
            article.author = article.author
    return article
