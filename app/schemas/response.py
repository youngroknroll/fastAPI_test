"""Response DTO 스키마들 - 데이터 전송용 (ORM 모델 격리)"""

from datetime import datetime
from pydantic import BaseModel

from app.models.user_model import User


# ============================================================================
# Author/User Response DTO
# ============================================================================

class AuthorResponse(BaseModel):
    """작성자 정보 응답"""
    username: str
    bio: str | None = None
    image: str | None = None
    following: bool = False

    @classmethod
    def from_user(cls, user: User, following: bool = False) -> "AuthorResponse":
        """User ORM 모델에서 AuthorResponse 생성"""
        return cls(
            username=user.username,
            bio=user.bio,
            image=user.image,
            following=following,
        )


class UserResponse(BaseModel):
    """유저 정보 응답"""
    email: str
    username: str
    token: str
    bio: str | None = None
    image: str | None = None

    @classmethod
    def from_user(cls, user: User, token: str) -> "UserResponse":
        """User ORM 모델에서 UserResponse 생성"""
        return cls(
            email=user.email,
            username=user.username,
            token=token,
            bio=user.bio,
            image=user.image,
        )


class ProfileResponse(BaseModel):
    """프로필 응답"""
    username: str
    bio: str | None = None
    image: str | None = None
    following: bool = False

    @classmethod
    def from_user(cls, user: User, following: bool = False) -> "ProfileResponse":
        """User ORM 모델에서 ProfileResponse 생성"""
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
    """게시글 응답"""
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


# ============================================================================
# Comment Response DTO
# ============================================================================

class CommentResponse(BaseModel):
    """댓글 응답"""
    id: int
    body: str
    createdAt: str  # ISO format with Z
    updatedAt: str  # ISO format with Z
    author: AuthorResponse
