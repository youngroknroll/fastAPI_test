"""User Service - 유저 비즈니스 로직"""

from typing import Optional

from fastapi import HTTPException

from app.core.security import create_access_token
from app.models.user_model import User
from app.repositories.interfaces import UserRepositoryInterface
from app.schemas.user_schema import UserRegister, UserUpdate


class UserService:
    """유저 관련 비즈니스 로직 처리"""

    def __init__(self, user_repo: UserRepositoryInterface):
        self._repo = user_repo

    def register_user(self, user_data: UserRegister) -> dict:
        """회원가입"""
        if self._repo.get_by_email(user_data.email):
            raise HTTPException(status_code=422, detail="Email already registered")

        user = self._repo.create(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
        )
        return self._build_user_response(user)

    def login_user(self, email: str, password: str) -> dict:
        """로그인"""
        user = self._repo.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=422, detail="Email not found")

        if user.hashed_password != password:
            raise HTTPException(status_code=422, detail="Invalid password")

        return self._build_user_response(user)

    def get_user_profile(self, user: User) -> dict:
        """내 정보 조회"""
        return self._build_user_response(user)

    def update_user(self, user: User, update_data: UserUpdate) -> dict:
        """내 정보 수정"""
        if update_data.email is not None:
            user.email = update_data.email
        if update_data.username is not None:
            user.username = update_data.username
        if update_data.password is not None:
            user.hashed_password = update_data.password
        if update_data.bio is not None:
            user.bio = update_data.bio
        if update_data.image is not None:
            user.image = update_data.image

        user = self._repo.update(user)
        return self._build_user_response(user)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """ID로 유저 조회"""
        return self._repo.get_by_id(user_id)

    def _build_user_response(self, user: User) -> dict:
        """유저 응답 형식 생성"""
        token = create_access_token(user_id=user.id, username=user.username)
        return {
            "user": {
                "email": user.email,
                "username": user.username,
                "token": token,
            }
        }
