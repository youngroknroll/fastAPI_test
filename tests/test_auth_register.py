"""Auth: Register Tests"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_올바른_요청을_보내면_새_유저_객체를_반환한다():
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


def test_반환된_유저_객체는_email을_포함한다():
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
    assert data["user"]["email"] == "test@example.com"


def test_반환된_유저_객체는_username을_포함한다():
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
    assert data["user"]["username"] == "testuser"


def test_반환된_유저_객체는_token을_포함한다():
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
    assert "token" in data["user"]
    assert isinstance(data["user"]["token"], str)
    assert len(data["user"]["token"]) > 0