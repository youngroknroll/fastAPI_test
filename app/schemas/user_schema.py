"""User Schemas"""

from typing import Optional

from pydantic import BaseModel


class UserRegister(BaseModel):
    """User registration request"""

    email: str
    password: str
    username: str


class UserLogin(BaseModel):
    """User login request"""

    email: str
    password: str


class UserUpdate(BaseModel):
    """User update request"""

    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None


class UserResponse(BaseModel):
    """User response"""

    email: str
    username: str
    token: str

