"""Auth: Get Current User Tests"""
from tests.conftest import Status
from tests.fixtures.auth_fixtures import DEFAULT_EMAIL, DEFAULT_USERNAME


def test_로그인한_유저는_내_정보를_조회할_수_있다(auth_api):
    auth_api.register()

    결과 = auth_api.userinfo()

    assert Status.of(결과) == Status.SUCCESS
    assert 결과.json()["user"]["email"] == DEFAULT_EMAIL
    assert 결과.json()["user"]["username"] == DEFAULT_USERNAME


def test_로그인하지_않으면_내_정보를_조회할_수_없다(auth_api):
    결과 = auth_api.userinfo()

    assert Status.of(결과) == Status.UNAUTHORIZED

