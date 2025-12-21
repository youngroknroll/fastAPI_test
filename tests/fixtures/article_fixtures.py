"""Article fixtures for tests"""

import pytest


@pytest.fixture(name="article_payload")
def article_payload():
    """기본 article 생성 payload"""
    payload = {
        "article": {"title": "Test Article", "description": "Test Desc", "body": "Test Body"}
    }
    return payload


class ArticleAPI:
    """Article API 헬퍼 클래스"""
    def __init__(self, client):
        self._client = client

    def create(self, payload, headers=None):
        return self._client.post("/articles", json=payload, headers=headers)

    def delete(self, slug, headers=None):
        return self._client.delete(f"/articles/{slug}", headers=headers)

    def get(self, slug, headers=None):
        return self._client.get(f"/articles/{slug}", headers=headers)


@pytest.fixture
def article_api(client):
    """ArticleAPI 인스턴스 반환"""
    return ArticleAPI(client)

