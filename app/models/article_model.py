from sqlmodel import Field, SQLModel

from app.models.base import TimestampModel


class Article(TimestampModel, table=True):

    __tablename__ = "articles"

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True)
    title: str
    description: str
    body: str
    author_id: int = Field(foreign_key="users.id")


