"""User fixtures for tests"""

import pytest



def _user1_token(client):
    """user1 등록 및 토큰 반환"""
    user1_payload = {
        "user": {"email": "user1@example.com", "password": "password123", "username": "user1"}
    }
    response = client.post("/users", json=user1_payload)
    token = response.json()["user"]["token"]
    return token



def _user2_token(client):
    """user2 등록 및 토큰 반환"""
    user2_payload = {
        "user": {"email": "user2@example.com", "password": "password123", "username": "user2"}
    }
    response = client.post("/users", json=user2_payload)
    token = response.json()["user"]["token"]
    return token


# 인증된 API fixtures

from tests.fixtures.article_fixtures import ArticleAPI

@pytest.fixture
def 로그인_유저1_api(client):
    """로그인한 유저1의 ArticleAPI"""
    return ArticleAPI(client, token=_user1_token(client))

@pytest.fixture
def 로그인_유저2_api(client):
    """로그인한 유저2의 ArticleAPI"""
    return ArticleAPI(client, token=_user2_token(client))

@pytest.fixture
def 게스트_api(client):
    """비로그인 유저의 API"""
    return ArticleAPI(client)