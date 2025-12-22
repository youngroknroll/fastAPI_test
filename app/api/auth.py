"""Auth API - 인증 관련 엔드포인트"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import get_current_user, get_user_service
from app.models.user_model import User
from app.schemas.user_schema import UserLogin, UserRegister, UserUpdate
from app.services.user_service import UserService

router = APIRouter(tags=["auth"])


# Request Wrappers
class UserRegisterRequest(BaseModel):
    user: UserRegister


class UserLoginRequest(BaseModel):
    user: UserLogin


class UserUpdateRequest(BaseModel):
    user: UserUpdate


# Endpoints
@router.post("/users", status_code=201)
def 회원가입(request: UserRegisterRequest, service: UserService = Depends(get_user_service)):
    return service.register_user(request.user)


@router.post("/users/login", status_code=200)
def 로그인(request: UserLoginRequest, service: UserService = Depends(get_user_service)):
    return service.login_user(request.user.email, request.user.password)


@router.get("/user", status_code=200)
def 내_정보_조회(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.get_user_profile(current_user)


@router.put("/user", status_code=200)
def 내_정보_수정(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.update_user(current_user, request.user)
