from fastapi import APIRouter, status
from typing import List


router = APIRouter()

articles_db: List[dict] = []


@router.post("", status_code=status.HTTP_201_CREATED)
def create_article(article: dict):
    articles_db.append(article)
    return article

@router.get("",status_code=status.HTTP_200_OK)
def list_articles():
    return articles_db