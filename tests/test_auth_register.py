"""Auth: Register Tests"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_returns_user_object():
    """올바른 요청을 보내면 새 유저 객체를 반환한다"""
    # given
    payload = {
        "user": {
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser",
        }
    }

    # when
    response = client.post("/users", json=payload)

    # then
    assert response.status_code == 201
    data = response.json()
    assert "user" in data

