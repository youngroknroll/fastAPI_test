"""User fixtures for tests"""

import pytest


@pytest.fixture
def user1_token(client):
    """user1 등록 및 토큰 반환"""
    user1_payload = {
        "user": {"email": "user1@example.com", "password": "password123", "username": "user1"}
    }
    response = client.post("/users", json=user1_payload)
    token = response.json()["user"]["token"]
    return token


@pytest.fixture
def user2_token(client):
    """user2 등록 및 토큰 반환"""
    user2_payload = {
        "user": {"email": "user2@example.com", "password": "password123", "username": "user2"}
    }
    response = client.post("/users", json=user2_payload)
    token = response.json()["user"]["token"]
    return token


@pytest.fixture(name="user1_header")
def user1_header(user1_payload):
    """user1 인증 헤더"""
    headers = {"Authorization": f"Token {user1_payload}"}
    return headers


@pytest.fixture(name="user2_header")
def user2_header(user2_payload):
    """user2 인증 헤더"""
    headers = {"Authorization": f"Token {user2_payload}"}
    return headers

