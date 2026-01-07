from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_user_service
from app.models.user_model import User
from app.dtos.request import UserRegisterRequest, UserLoginRequest, UserUpdateRequest
from app.services.user_service import UserService

router = APIRouter(tags=["auth"])


@router.post("/users", status_code=201)
def register(request: UserRegisterRequest, service: UserService = Depends(get_user_service)):
    return service.register_user(request.user)


@router.post("/users/login", status_code=200)
def login(request: UserLoginRequest, service: UserService = Depends(get_user_service)):
    return service.login_user(request.user.email, request.user.password)


@router.get("/user", status_code=200)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.get_user_profile(current_user)


@router.put("/user", status_code=200)
def update_user(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.update_user(current_user, request.user)
