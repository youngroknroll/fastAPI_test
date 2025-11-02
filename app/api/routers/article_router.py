from fastapi import APIRouter, status

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_article(article: dict):
    return article