from typing import List

from fastapi import APIRouter, Depends

from app.core.db import get_article_service
from app.schemas.article_schema import ArticleResponse, ArticleUpdate, ArticleCreate
from app.services.article_service import ArticleService

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/", response_model=List[ArticleResponse])
def list_articles(service: ArticleService = Depends(get_article_service)):
    """글 목록 조회"""
    return service.list_articles()

@router.get("/{id}", response_model=ArticleResponse)
def get_article(id: int, service: ArticleService = Depends(get_article_service)):
    return service.get_article(id)

@router.post("/", response_model=ArticleResponse, status_code=201)
def create_article(request: ArticleCreate, service: ArticleService = Depends(get_article_service)):
    return service.create_article(request)

@router.put("/{id}", response_model=ArticleResponse)
def update_article(id: int, request:ArticleUpdate, service: ArticleService = Depends(get_article_service)):
    """수정"""
    return service.update_article(id, request)

@router.delete("/{id}", status_code=204)
def delete_article(id: int, service: ArticleService = Depends(get_article_service)):
    """삭제"""
    service.delete_article(id)