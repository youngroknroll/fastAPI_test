from pydantic import BaseModel

from app.schemas.user_schema import UserLogin, UserRegister, UserUpdate
from app.schemas.article_schema import ArticleCreate, ArticleUpdate


# ============================================================================
# Auth API Request DTOs
# ============================================================================

class UserRegisterRequest(BaseModel):
    user: UserRegister


class UserLoginRequest(BaseModel):
    user: UserLogin


class UserUpdateRequest(BaseModel):
    user: UserUpdate


# ============================================================================
# Article API Request DTOs
# ============================================================================

class ArticleCreateRequest(BaseModel):
    article: ArticleCreate


class ArticleUpdateRequest(BaseModel):
    article: ArticleUpdate


# ============================================================================
# Comment API Request DTOs
# ============================================================================

class CommentCreate(BaseModel):
    body: str


class CommentCreateRequest(BaseModel):
    comment: CommentCreate
