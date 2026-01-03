from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    description: str
    body: str
    tagList: list[str] | None = None


class ArticleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    body: str | None = None
