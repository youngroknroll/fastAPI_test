from sqlmodel import Session
from fastapi import HTTPException

from app.repositories.article_repo import Article, ArticleRepo
from app.schemas.article_schema import ArticleCreate, ArticleUpdate, ArticleResponse

class ArticleService:
    # 비즈니스 로직
    def __init__(self, session: Session):
        self.repo = ArticleRepo(session)

    def list_articles(self):
        """글 목록"""
        articles =self.repo.list()
        return [ArticleResponse.model_validate(article) for article in articles]

    def get_article(self, article_id: int):
        """조회"""
        article = self.repo.get(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="ARTICLE NOT FOUND")
        return ArticleResponse.model_validate(article)

    def create_article(self, request: ArticleCreate):
        """생성"""
        article = Article(title=request.title, author=request.author)
        created = self.repo.create(article)
        return ArticleResponse.model_validate(created)

    def update_article(self, article_id: int, request: ArticleUpdate):
        """수정"""
        article = self.repo.get(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="ARTICLE NOT FOUND")

        article.title = request.title
        article.author = request.author

        updated = self.repo.update(article)
        return ArticleResponse.model_validate(updated)

    def delete_article(self, article_id: int):
        """삭제"""
        article = self.repo.get(article_id)
        self.repo.delete(article)
