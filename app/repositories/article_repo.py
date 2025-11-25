from sqlmodel import Session, select

from app.models.article_model import Article


class ArticleRepo:
    """순수 데이터 접근 레이어"""

    def __init__(self, session: Session):
        self.session = session

    def list(self) -> list[Article]:
        """전체 목록 조회"""
        statement = select(Article)
        return self.session.exec(statement).all()

    def get(self, article_id: int) -> Article | None:
        """ID로 단건 조회"""
        return self.session.get(Article, article_id)

    def create(self, title: str, author: str) -> Article:
        """게시글 생성"""
        article = Article(title=title, author=author)
        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)
        return article

    def update(self, article_id: int, title: str, author: str) -> Article | None:
        """게시글 수정"""
        article = self.get(article_id)
        if not article:
            return None

        article.title = title
        article.author = author

        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)
        return article

    def delete(self, article_id: int) -> bool:
        """게시글 삭제"""
        article = self.get(article_id)
        if not article:
            return False

        self.session.delete(article)
        self.session.commit()
        return True
