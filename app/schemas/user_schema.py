from pydantic import BaseModel


class UserRegister(BaseModel):

    email: str
    password: str
    username: str


class UserLogin(BaseModel):

    email: str
    password: str


class UserUpdate(BaseModel):

    email: str | None = None
    username: str | None = None
    password: str | None = None
    bio: str | None = None
    image: str | None = None


class UserResponse(BaseModel):

    email: str
    username: str
    token: str

