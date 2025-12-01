"""Profiles Tests"""


def test_존재하는_username으로_프로필을_조회하면_profile_객체를_반환한다(client):
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

    # then: profile 객체를 반환
    assert response.status_code == 200
    data = response.json()
    assert "profile" in data


def test_로그인하지_않아도_프로필_조회가_가능하다(client):
    # given: 유저를 등록
    register_payload = {
        "user": {
            "email": "public@example.com",
            "password": "password123",
            "username": "publicuser",
        }
    }
    client.post("/users", json=register_payload)

    # when: Authorization 헤더 없이 프로필 조회
    response = client.get("/profiles/publicuser")

    # then: 200 반환
    assert response.status_code == 200
    data = response.json()
    assert "profile" in data
    assert data["profile"]["username"] == "publicuser"


def test_follow_요청을_보내면_following_true를_반환한다(client):
    # given: 두 명의 유저를 등록 (팔로워, 팔로이)
    follower_payload = {
        "user": {"email": "follower@example.com", "password": "password123", "username": "follower"}
    }
    followee_payload = {
        "user": {"email": "followee@example.com", "password": "password123", "username": "followee"}
    }
    follower_response = client.post("/users", json=follower_payload)
    client.post("/users", json=followee_payload)

    follower_token = follower_response.json()["user"]["token"]

    # when: follower가 followee를 follow
    headers = {"Authorization": f"Token {follower_token}"}
    response = client.post("/profiles/followee/follow", headers=headers)

    # then: following이 true
    assert response.status_code == 200
    data = response.json()
    assert data["profile"]["following"] is True


def test_unfollow_요청을_보내면_following_false를_반환한다(client):
    # given: 두 명의 유저를 등록하고 follow 관계 생성
    follower_payload = {
        "user": {"email": "unfollower@example.com", "password": "password123", "username": "unfollower"}
    }
    followee_payload = {
        "user": {"email": "unfollowee@example.com", "password": "password123", "username": "unfollowee"}
    }
    follower_response = client.post("/users", json=follower_payload)
    client.post("/users", json=followee_payload)

    follower_token = follower_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {follower_token}"}

    # follow first
    client.post("/profiles/unfollowee/follow", headers=headers)

    # when: unfollow
    response = client.delete("/profiles/unfollowee/follow", headers=headers)

    # then: following이 false
    assert response.status_code == 200
    data = response.json()
    assert data["profile"]["following"] is False


def test_자신을_follow_하려고_하면_422를_반환한다(client):
    # given: 유저를 등록
    user_payload = {
        "user": {"email": "self@example.com", "password": "password123", "username": "selfuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]

    # when: 자기 자신을 follow 시도
    headers = {"Authorization": f"Token {token}"}
    response = client.post("/profiles/selfuser/follow", headers=headers)

    # then: 422 반환
    assert response.status_code == 422

