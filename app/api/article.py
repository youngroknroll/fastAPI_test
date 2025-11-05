from fastapi import APIRouter, HTTPException

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

