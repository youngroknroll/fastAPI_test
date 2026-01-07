from fastapi import HTTPException

from app.models.article_model import Article
from app.models.user_model import User
from app.repositories.interfaces import ArticleRepositoryInterface, UserRepositoryInterface


def get_article_or_404(article_repo: ArticleRepositoryInterface, slug: str) -> Article:
    article = article_repo.get_by_slug(slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


def get_user_or_404(user_repo: UserRepositoryInterface, username: str) -> User:
    user = user_repo.get_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return user


def check_author_permission(article: Article, user: User) -> None:
    if article.author_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the author of this article")


def check_comment_author_permission(comment_author_id: int, user_id: int) -> None:
    if comment_author_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the author of this comment")
