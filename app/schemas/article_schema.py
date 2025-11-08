from pydantic import BaseModel

class ArticleCreate(BaseModel):
    title: str
    author: str

class ArticleResponse(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        from_attributes = True

class ArticleUpdate(BaseModel):
    title: str
    author: str



