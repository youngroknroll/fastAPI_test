"""Auth: Login Tests"""


def test_올바른_email과_password로_로그인하면_유저_객체를_반환한다(client):
    # given: 먼저 유저를 등록
    register_payload = {
        "user": {
            "email": "login@example.com",
            "password": "password123",
            "username": "loginuser",
        }
    }
    client.post("/users", json=register_payload)

    # when: 같은 email과 password로 로그인
    login_payload = {"user": {"email": "login@example.com", "password": "password123"}}
    response = client.post("/users/login", json=login_payload)

    # then
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "login@example.com"


def test_잘못된_password면_422를_반환한다(client):
    # given: 먼저 유저를 등록
    register_payload = {
        "user": {
            "email": "test@example.com",
            "password": "correct_password",
            "username": "testuser",
        }
    }
    client.post("/users", json=register_payload)

    # when: 잘못된 password로 로그인 시도
    login_payload = {"user": {"email": "test@example.com", "password": "wrong_password"}}
    response = client.post("/users/login", json=login_payload)

    # then
    assert response.status_code == 422


def test_존재하지_않는_email이면_422를_반환한다(client):
    # given: 등록되지 않은 email

    # when: 존재하지 않는 email로 로그인 시도
    login_payload = {
        "user": {"email": "nonexistent@example.com", "password": "any_password"}
    }
    response = client.post("/users/login", json=login_payload)

    # then
    assert response.status_code == 422

