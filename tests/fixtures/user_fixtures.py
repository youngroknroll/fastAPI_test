"""User fixtures for tests"""

import pytest

from tests.fixtures.article_fixtures import ArticleAPI
from tests.fixtures.auth_fixtures import AuthAPI


def _register_user(client, email, password, username):
    """유저 등록 후 토큰 반환"""
    auth = AuthAPI(client)
    auth.register(email=email, password=password, username=username)
    return auth.token


@pytest.fixture
def 로그인_유저1_api(client):
    """로그인한 유저1의 ArticleAPI"""
    token = _register_user(client, "user1@example.com", "password123", "user1")
    return ArticleAPI(client, token=token)


@pytest.fixture
def 로그인_유저2_api(client):
    """로그인한 유저2의 ArticleAPI"""
    token = _register_user(client, "user2@example.com", "password123", "user2")
    return ArticleAPI(client, token=token)


@pytest.fixture
def 게스트_api(client):
    """비로그인 유저의 API"""
    return ArticleAPI(client)