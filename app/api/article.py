"""Article API Router"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.article_schema import ArticleCreate, ArticleUpdate
from app.services.article_service import ArticleService

router = APIRouter(tags=["articles"])


class ArticleCreateRequest(BaseModel):
    """Article create request wrapper"""

    article: ArticleCreate


class ArticleUpdateRequest(BaseModel):
    """Article update request wrapper"""

    article: ArticleUpdate


@router.get("/articles", status_code=200)
def get_articles(
    author: str = None,
    tag: str = None,
    favorited: str = None,
    session: Session = Depends(get_session),
):
    """Get articles"""
    service = ArticleService(session)
    return service.get_articles(author=author, tag=tag, favorited=favorited)


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
        tag_list=request.article.tagList,
    )


@router.get("/articles/{slug}", status_code=200)
def get_article(slug: str, session: Session = Depends(get_session)):
    """Get article by slug"""
    service = ArticleService(session)
    return service.get_article_by_slug(slug)


@router.put("/articles/{slug}", status_code=200)
def update_article(
    slug: str,
    request: ArticleUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update an article"""
    service = ArticleService(session)
    return service.update_article(
        slug=slug,
        user=current_user,
        title=request.article.title,
        description=request.article.description,
        body=request.article.body,
    )


@router.delete("/articles/{slug}", status_code=204)
def delete_article(
    slug: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete an article"""
    service = ArticleService(session)
    service.delete_article(slug=slug, user=current_user)


@router.post("/articles/{slug}/favorite", status_code=200)
def favorite_article(
    slug: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Favorite an article"""
    service = ArticleService(session)
    return service.favorite_article(slug=slug, user=current_user)

