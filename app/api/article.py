from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel


#basemodel
class Article(SQLModel):
    id: int | None = None
    title: str
    author: str
router = APIRouter(prefix="/articles", tags=["articles"])

articles = [
        {"id": 1, "title": "첫 번째 글", "author": "영록"},
        {"id": 2, "title": "두 번째 글", "author": "익명"},
    ]

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