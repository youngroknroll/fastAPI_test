"""Profiles Tests"""
from tests.conftest import Status
from tests.fixtures.auth_fixtures import AuthAPI


def test_다른_유저의_프로필을_조회할_수_있다(auth_api):
    auth_api.register(username="profileuser")

    결과 = auth_api.get_profile("profileuser")

    assert Status.of(결과) == Status.SUCCESS
    assert "profile" in 결과.json()


def test_로그인하지_않아도_프로필을_조회할_수_있다(client):
    # 유저 등록
    auth = AuthAPI(client)
    auth.register(username="publicuser")

    # 비로그인 상태로 프로필 조회
    guest = AuthAPI(client)
    결과 = guest.get_profile("publicuser")

    assert Status.of(결과) == Status.SUCCESS
    assert 결과.json()["profile"]["username"] == "publicuser"


def test_다른_유저를_팔로우할_수_있다(client):
    # 팔로워 등록
    팔로워 = AuthAPI(client)
    팔로워.register(email="follower@example.com", username="follower")

    # 팔로이 등록
    팔로이 = AuthAPI(client)
    팔로이.register(email="followee@example.com", username="followee")

    # 팔로우
    결과 = 팔로워.follow("followee")

    assert Status.of(결과) == Status.SUCCESS
    assert 결과.json()["profile"]["following"] is True


def test_팔로우를_취소할_수_있다(client):
    # 팔로워 등록
    팔로워 = AuthAPI(client)
    팔로워.register(email="unfollower@example.com", username="unfollower")

    # 팔로이 등록
    팔로이 = AuthAPI(client)
    팔로이.register(email="unfollowee@example.com", username="unfollowee")

    # 팔로우 후 언팔로우
    팔로워.follow("unfollowee")
    결과 = 팔로워.unfollow("unfollowee")

    assert Status.of(결과) == Status.SUCCESS
    assert 결과.json()["profile"]["following"] is False


def test_자기_자신은_팔로우할_수_없다(auth_api):
    auth_api.register(username="selfuser")

    결과 = auth_api.follow("selfuser")

    assert Status.of(결과) == Status.VALIDATION_ERROR
