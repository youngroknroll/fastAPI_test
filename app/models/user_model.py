from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    bio: str | None = None
    image: str | None = None

