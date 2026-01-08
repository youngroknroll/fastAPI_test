from fastapi import APIRouter, Depends

from app.core.dependencies import get_article_service, get_current_user, get_current_user_optional
from app.models.user_model import User
from app.dtos.request import ArticleCreateRequest, ArticleUpdateRequest
from app.dtos.response import ArticleResponseWrapper, SingleArticleResponseWrapper
from app.services.article_service import ArticleService

router = APIRouter(tags=["articles"])


@router.get("/articles", status_code=200, response_model=ArticleResponseWrapper)
def get_articles(
    author: str = None,
    tag: str = None,
    favorited: str = None,
    current_user: User | None = Depends(get_current_user_optional),
    service: ArticleService = Depends(get_article_service),
):
    current_user_id = current_user.id if current_user else None
    return service.get_articles(author=author, tag=tag, favorited=favorited, current_user_id=current_user_id)


@router.post("/articles", status_code=201, response_model=SingleArticleResponseWrapper)
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


@router.get("/articles/{slug}", status_code=200, response_model=SingleArticleResponseWrapper)
def get_article(
    slug: str,
    current_user: User | None = Depends(get_current_user_optional),
    service: ArticleService = Depends(get_article_service),
):
    current_user_id = current_user.id if current_user else None
    article_dto = service.get_article_by_slug(slug, current_user_id=current_user_id)
    return {"article": article_dto}


@router.put("/articles/{slug}", status_code=200, response_model=SingleArticleResponseWrapper)
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


@router.post("/articles/{slug}/favorite", status_code=200, response_model=SingleArticleResponseWrapper)
def favorite_article(
    slug: str,
    current_user: User = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    article_dto = service.favorite_article(slug=slug, user=current_user)
    return {"article": article_dto}


@router.delete("/articles/{slug}/favorite", status_code=200, response_model=SingleArticleResponseWrapper)
def unfavorite_article(
    slug: str,
    current_user: User = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    article_dto = service.unfavorite_article(slug=slug, user=current_user)
    return {"article": article_dto}
