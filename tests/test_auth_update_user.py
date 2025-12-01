"""Auth: Update User Tests"""


def test_올바른_토큰으로_user_정보를_수정할_수_있다(client):
    # given: 유저를 등록하고 토큰을 받음
    register_payload = {
        "user": {
            "email": "update@example.com",
            "password": "password123",
            "username": "updateuser",
        }
    }
    register_response = client.post("/users", json=register_payload)
    token = register_response.json()["user"]["token"]

    # when: Authorization 헤더와 함께 유저 정보 수정 요청
    headers = {"Authorization": f"Token {token}"}
    update_payload = {"user": {"username": "newusername", "email": "newemail@example.com"}}
    response = client.put("/user", json=update_payload, headers=headers)

    # then
    assert response.status_code == 200
    data = response.json()
    assert "user" in data


def test_수정된_필드는_응답에서도_반영된다(client):
    # given: 유저를 등록하고 토큰을 받음
    register_payload = {
        "user": {
            "email": "original@example.com",
            "password": "password123",
            "username": "originaluser",
        }
    }
    register_response = client.post("/users", json=register_payload)
    token = register_response.json()["user"]["token"]

    # when: 필드를 수정
    headers = {"Authorization": f"Token {token}"}
    update_payload = {"user": {"username": "modifieduser", "email": "modified@example.com"}}
    response = client.put("/user", json=update_payload, headers=headers)

    # then: 응답의 필드가 수정된 값과 일치
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "modifieduser"
    assert data["user"]["email"] == "modified@example.com"


def test_토큰_없이_요청하면_401을_반환한다(client):
    # given: 유저 정보 수정 페이로드
    update_payload = {"user": {"username": "newusername"}}

    # when: Authorization 헤더 없이 요청
    response = client.put("/user", json=update_payload)

    # then
    assert response.status_code == 401

