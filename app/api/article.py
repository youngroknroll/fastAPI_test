from fastapi import APIRouter, Depends

from app.core.dependencies import get_article_service, get_current_user
from app.models.user_model import User
from app.dtos.request import ArticleCreateRequest, ArticleUpdateRequest
from app.services.article_service import ArticleService

router = APIRouter(tags=["articles"])


@router.get("/articles", status_code=200)
def get_articles(
    author: str = None,
    tag: str = None,
    favorited: str = None,
    service: ArticleService = Depends(get_article_service),
):
    return service.get_articles(author=author, tag=tag, favorited=favorited)


@router.post("/articles", status_code=201)
def create_article(
    request: ArticleCreateRequest,
    current_user: User = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    article_dto = service.create_article(
        title=request.article.title,
        description=request.article.description,
        body=request.article.body,
        author=current_user,
        tag_list=request.article.tagList,
    )
    return {"article": article_dto}


@router.get("/articles/{slug}", status_code=200)
def get_article(slug: str, service: ArticleService = Depends(get_article_service)):
    article_dto = service.get_article_by_slug(slug)
    return {"article": article_dto}


@router.put("/articles/{slug}", status_code=200)
def update_article(
    slug: str,
    request: ArticleUpdateRequest,
    current_user: User = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    article_dto = service.update_article(
        slug=slug,
        user=current_user,
        title=request.article.title,
        description=request.article.description,
        body=request.article.body,
    )
    return {"article": article_dto}


@router.delete("/articles/{slug}", status_code=204)
def delete_article(
    slug: str,
    current_user: User = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    service.delete_article(slug=slug, user=current_user)


@router.post("/articles/{slug}/favorite", status_code=200)
def favorite_article(
    slug: str,
    current_user: User = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    article_dto = service.favorite_article(slug=slug, user=current_user)
    return {"article": article_dto}


@router.delete("/articles/{slug}/favorite", status_code=200)
def unfavorite_article(
    slug: str,
    current_user: User = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    article_dto = service.unfavorite_article(slug=slug, user=current_user)
    return {"article": article_dto}
