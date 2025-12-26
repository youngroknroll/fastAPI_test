from tests.conftest import Status
from tests.fixtures.auth_fixtures import DEFAULT_EMAIL


def test_올바른_이메일과_비밀번호로_로그인할_수_있다(auth_api):
    auth_api.register()

    결과 = auth_api.login()

    assert Status.of(결과) == Status.SUCCESS
    assert 결과.json()["user"]["email"] == DEFAULT_EMAIL


def test_잘못된_비밀번호로는_로그인할_수_없다(auth_api):
    auth_api.register()

    결과 = auth_api.login(password="wrong_password")

    assert Status.of(결과) == Status.VALIDATION_ERROR


def test_존재하지_않는_이메일로는_로그인할_수_없다(auth_api):
    결과 = auth_api.login(email="nonexistent@example.com")

    assert Status.of(결과) == Status.VALIDATION_ERROR

