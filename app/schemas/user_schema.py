"""User Schemas"""

from pydantic import BaseModel


class UserRegister(BaseModel):
    """User registration request"""

    email: str
    password: str
    username: str


class UserResponse(BaseModel):
    """User response"""

    email: str
    username: str
    token: str

