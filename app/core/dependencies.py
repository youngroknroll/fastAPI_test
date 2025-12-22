"""FastAPI Dependencies - 의존성 주입 설정"""

from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import verify_token
from app.models.user_model import User
from app.repositories.interfaces import (
    ArticleRepositoryInterface,
    FavoriteRepositoryInterface,
    TagRepositoryInterface,
    UserRepositoryInterface,
)
from app.repositories.article_repository import ArticleRepository
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.tag_repository import TagRepository
from app.repositories.user_repository import UserRepository
from app.services.article_service import ArticleService
from app.services.user_service import UserService


# Repository
def get_user_repository(session: Session = Depends(get_session)) -> UserRepositoryInterface:
    return UserRepository(session)


def get_article_repository(session: Session = Depends(get_session)) -> ArticleRepositoryInterface:
    return ArticleRepository(session)


def get_tag_repository(session: Session = Depends(get_session)) -> TagRepositoryInterface:
    return TagRepository(session)


def get_favorite_repository(session: Session = Depends(get_session)) -> FavoriteRepositoryInterface:
    return FavoriteRepository(session)


# Service
def get_user_service(user_repo: UserRepositoryInterface = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)


def get_article_service(
    article_repo: ArticleRepositoryInterface = Depends(get_article_repository),
    user_repo: UserRepositoryInterface = Depends(get_user_repository),
    tag_repo: TagRepositoryInterface = Depends(get_tag_repository),
    favorite_repo: FavoriteRepositoryInterface = Depends(get_favorite_repository),
) -> ArticleService:
    return ArticleService(article_repo, user_repo, tag_repo, favorite_repo)


# Auth
def get_current_user(
    authorization: Optional[str] = Header(None),
    user_repo: UserRepositoryInterface = Depends(get_user_repository),
) -> User:
    """JWT 토큰에서 현재 로그인한 유저 조회"""
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.replace("Token ", "")

    try:
        payload = verify_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    user = user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    user_repo: UserRepositoryInterface = Depends(get_user_repository),
) -> Optional[User]:
    """JWT 토큰에서 현재 유저 조회 (선택적 - 비로그인 허용 엔드포인트용)"""
    if authorization is None:
        return None

    try:
        return get_current_user(authorization, user_repo)
    except HTTPException:
        return None
