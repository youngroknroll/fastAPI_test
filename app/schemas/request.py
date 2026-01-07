"""API Request/Response wrapper models - 중앙집중식 관리"""

from pydantic import BaseModel

from app.schemas.user_schema import UserLogin, UserRegister, UserUpdate
from app.schemas.article_schema import ArticleCreate, ArticleUpdate


# ============================================================================
# Auth API Request Wrappers
# ============================================================================

class UserRegisterRequest(BaseModel):
    """회원가입 요청"""

    user: UserRegister


class UserLoginRequest(BaseModel):
    """로그인 요청"""

    user: UserLogin


class UserUpdateRequest(BaseModel):
    """유저 정보 수정 요청"""

    user: UserUpdate


# ============================================================================
# Article API Request Wrappers
# ============================================================================

class ArticleCreateRequest(BaseModel):
    """게시글 생성 요청"""

    article: ArticleCreate


class ArticleUpdateRequest(BaseModel):
    """게시글 수정 요청"""

    article: ArticleUpdate


# ============================================================================
# Comment API Request Wrappers
# ============================================================================

class CommentCreate(BaseModel):
    """댓글 내용"""

    body: str


class CommentCreateRequest(BaseModel):
    """댓글 생성 요청"""

    comment: CommentCreate
