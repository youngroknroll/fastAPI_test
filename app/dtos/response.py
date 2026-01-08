from datetime import datetime
from pydantic import BaseModel

from app.models.user_model import User


# ============================================================================
# Author/User Response DTOs
# ============================================================================

class AuthorResponse(BaseModel):
    username: str
    bio: str | None = None
    image: str | None = None
    following: bool = False

    @classmethod
    def from_user(cls, user: User, following: bool = False) -> "AuthorResponse":
        return cls(
            username=user.username,
            bio=user.bio,
            image=user.image,
            following=following,
        )


class UserResponse(BaseModel):
    email: str
    username: str
    token: str
    bio: str | None = None
    image: str | None = None

    @classmethod
    def from_user(cls, user: User, token: str) -> "UserResponse":
        return cls(
            email=user.email,
            username=user.username,
            token=token,
            bio=user.bio,
            image=user.image,
        )


class ProfileResponse(BaseModel):
    username: str
    bio: str | None = None
    image: str | None = None
    following: bool = False

    @classmethod
    def from_user(cls, user: User, following: bool = False) -> "ProfileResponse":
        return cls(
            username=user.username,
            bio=user.bio,
            image=user.image,
            following=following,
        )


# ============================================================================
# Article Response DTO
# ============================================================================

class ArticleResponse(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tagList: list[str]
    createdAt: str  # ISO format with Z
    updatedAt: str  # ISO format with Z
    favoritesCount: int
    favorited: bool
    author: AuthorResponse

    @classmethod
    def from_article_data(cls, article_data: dict) -> "ArticleResponse":
        """리포지토리에서 받은 관계 데이터로 응답 생성"""
        article = article_data['article']
        author = article_data['author']
        tag_list = article_data.get('tag_list', [])
        favorites_count = article_data.get('favorites_count', 0)
        favorited = article_data.get('favorited', False)
        
        return cls(
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            tagList=tag_list,
            createdAt=article.created_at.isoformat() + "Z",
            updatedAt=article.updated_at.isoformat() + "Z",
            favoritesCount=favorites_count,
            favorited=favorited,
            author=AuthorResponse.from_user(author),
        )


# ============================================================================
# Comment Response DTO
# ============================================================================

class CommentResponse(BaseModel):
    id: int
    body: str
    createdAt: str  # ISO format with Z
    updatedAt: str  # ISO format with Z
    author: AuthorResponse
