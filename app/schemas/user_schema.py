from typing import Optional

from pydantic import BaseModel


class UserRegister(BaseModel):

    email: str
    password: str
    username: str


class UserLogin(BaseModel):

    email: str
    password: str


class UserUpdate(BaseModel):

    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None


class UserResponse(BaseModel):

    email: str
    username: str
    token: str

