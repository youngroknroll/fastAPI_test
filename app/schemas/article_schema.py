from pydantic import BaseModel, ConfigDict
class ArticleCreate(BaseModel):
    title: str
    author: str

class ArticleResponse(BaseModel):
    id: int
    title: str
    author: str

    model_config = ConfigDict(from_attributes=True)

class ArticleUpdate(BaseModel):
    title: str
    author: str



