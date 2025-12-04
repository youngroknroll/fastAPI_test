"""Article API Router"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.article_schema import ArticleCreate
from app.services.article_service import ArticleService

router = APIRouter(tags=["articles"])


class ArticleCreateRequest(BaseModel):
    """Article create request wrapper"""

    article: ArticleCreate


@router.get("/articles", status_code=200)
def get_articles(session: Session = Depends(get_session)):
    """Get articles"""
    service = ArticleService(session)
    return service.get_articles()


@router.post("/articles", status_code=201)
def create_article(
    request: ArticleCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create article"""
    service = ArticleService(session)
    return service.create_article(
        title=request.article.title,
        description=request.article.description,
        body=request.article.body,
        author=current_user,
    )


@router.get("/articles/{slug}", status_code=200)
def get_article(slug: str, session: Session = Depends(get_session)):
    """Get article by slug"""
    service = ArticleService(session)
    return service.get_article_by_slug(slug)

