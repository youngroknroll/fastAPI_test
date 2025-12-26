from tests.conftest import Status


def test_로그인한_유저는_내_정보를_수정할_수_있다(auth_api):
    auth_api.register()

    결과 = auth_api.update(username="newusername", email="newemail@example.com")

    assert Status.of(결과) == Status.SUCCESS
    assert "user" in 결과.json()


def test_수정한_정보가_응답에_반영된다(auth_api):
    auth_api.register()

    결과 = auth_api.update(username="modifieduser", email="modified@example.com")

    assert Status.of(결과) == Status.SUCCESS
    assert 결과.json()["user"]["username"] == "modifieduser"
    assert 결과.json()["user"]["email"] == "modified@example.com"


def test_로그인하지_않으면_내_정보를_수정할_수_없다(auth_api):
    결과 = auth_api.update(username="newusername")

    assert Status.of(결과) == Status.UNAUTHORIZED

