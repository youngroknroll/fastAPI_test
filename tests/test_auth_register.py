"""Auth: Register Tests"""


def test_올바른_요청을_보내면_새_유저_객체를_반환한다(client):
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


def test_반환된_유저_객체는_email을_포함한다(client):
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


def test_반환된_유저_객체는_username을_포함한다(client):
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


def test_반환된_유저_객체는_token을_포함한다(client):
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


def test_이미_존재하는_이메일이면_422를_반환한다(client):
    # given: 먼저 유저를 등록
    payload = {
        "user": {
            "email": "duplicate@example.com",
            "password": "password123",
            "username": "user1",
        }
    }
    client.post("/users", json=payload)

    # when: 같은 이메일로 다시 등록 시도
    duplicate_payload = {
        "user": {
            "email": "duplicate@example.com",
            "password": "password456",
            "username": "user2",
        }
    }
    response = client.post("/users", json=duplicate_payload)

    # then
    assert response.status_code == 422


def test_비밀번호가_없으면_422를_반환한다(client):
    # given: 비밀번호 없는 요청
    payload = {"user": {"email": "test@example.com", "username": "testuser"}}

    # when
    response = client.post("/users", json=payload)

    # then
    assert response.status_code == 422


def test_username이_비어_있으면_422를_반환한다(client):
    # given: username 없는 요청
    payload = {"user": {"email": "test@example.com", "password": "password123"}}

    # when
    response = client.post("/users", json=payload)

    # then
    assert response.status_code == 422