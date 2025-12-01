"""Auth: Get Current User Tests"""


def test_Authorization_토큰이_있으면_현재_유저_정보를_반환한다(client):
    # given: 유저를 등록하고 토큰을 받음
    register_payload = {
        "user": {
            "email": "current@example.com",
            "password": "password123",
            "username": "currentuser",
        }
    }
    register_response = client.post("/users", json=register_payload)
    token = register_response.json()["user"]["token"]

    # when: Authorization 헤더에 토큰을 넣어서 현재 유저 정보 요청
    headers = {"Authorization": f"Token {token}"}
    response = client.get("/user", headers=headers)

    # then
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "current@example.com"
    assert data["user"]["username"] == "currentuser"


def test_Authorization_토큰이_없으면_401을_반환한다(client):
    # given: Authorization 헤더 없음

    # when: Authorization 헤더 없이 현재 유저 정보 요청
    response = client.get("/user")

    # then
    assert response.status_code == 401

