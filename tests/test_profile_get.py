"""Profile: Get Profile Tests"""


def test_존재하는_username으로_프로필을_조회할_수_있다(client):
    # given: 유저를 등록
    register_payload = {
        "user": {
            "email": "profile@example.com",
            "password": "password123",
            "username": "profileuser",
        }
    }
    client.post("/users", json=register_payload)

    # when: username으로 프로필 조회
    response = client.get("/profiles/profileuser")

    # then
    assert response.status_code == 200
    data = response.json()
    assert "profile" in data

