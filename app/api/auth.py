"""Auth API Router"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.user_schema import UserLogin, UserRegister, UserUpdate
from app.services.user_service import UserService

router = APIRouter(tags=["auth"])


class UserRegisterRequest(BaseModel):
    """Register request wrapper"""

    user: UserRegister


class UserLoginRequest(BaseModel):
    """Login request wrapper"""

    user: UserLogin


class UserUpdateRequest(BaseModel):
    """Update request wrapper"""

    user: UserUpdate


@router.post("/users", status_code=201)
def register(request: UserRegisterRequest, session: Session = Depends(get_session)):
    """Register a new user"""
    service = UserService(session)
    return service.register_user(request.user)


@router.post("/users/login", status_code=200)
def login(request: UserLoginRequest, session: Session = Depends(get_session)):
    """Login user"""
    service = UserService(session)
    return service.login_user(request.user.email, request.user.password)


@router.get("/user", status_code=200)
def get_current_user_endpoint(
    current_user: User = Depends(get_current_user), session: Session = Depends(get_session)
):
    """Get current user"""
    service = UserService(session)
    return service.get_user_profile(current_user)


@router.put("/user", status_code=200)
def update_user(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update user"""
    service = UserService(session)
    return service.update_user(current_user, request.user)

