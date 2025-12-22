"""Article fixtures for tests"""

import pytest

class ArticleAPI:
    """Article API 헬퍼 클래스"""
    def __init__(self, client, token=None):
        self._client = client
        self._token = token

    def _get_headers(self):
        if self._token:
            return {"Authorization": f"Token {self._token}"}
        return None

    def create(self, payload):
        return self._client.post("/articles", json=payload, headers=self._get_headers())

    def delete(self, slug):
        return self._client.delete(f"/articles/{slug}", headers=self._get_headers())

    def get(self, slug):
        return self._client.get(f"/articles/{slug}", headers=self._get_headers())

    def update(self, slug, payload):
        return self._client.put(f"/articles/{slug}", json=payload, headers=self._get_headers())

    def list(self, **params):
        return self._client.get("/articles", params=params, headers=self._get_headers())

    def favorite(self, slug):
        return self._client.post(f"/articles/{slug}/favorite", headers=self._get_headers())

    def unfavorite(self, slug):
        return self._client.delete(f"/articles/{slug}/favorite", headers=self._get_headers())


@pytest.fixture
def article_api(client):
    """ArticleAPI 인스턴스 반환"""
    return ArticleAPI(client)