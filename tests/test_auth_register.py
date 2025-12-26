from tests.conftest import Status
from tests.fixtures.auth_fixtures import DEFAULT_EMAIL, DEFAULT_USERNAME


def test_회원가입하면_유저_정보를_반환한다(auth_api):
    결과 = auth_api.register()

    assert Status.of(결과) == Status.CREATED
    assert "user" in 결과.json()


def test_회원가입하면_입력한_이메일이_저장된다(auth_api):
    결과 = auth_api.register()

    assert Status.of(결과) == Status.CREATED
    assert 결과.json()["user"]["email"] == DEFAULT_EMAIL


def test_회원가입하면_입력한_username이_저장된다(auth_api):
    결과 = auth_api.register()

    assert Status.of(결과) == Status.CREATED
    assert 결과.json()["user"]["username"] == DEFAULT_USERNAME


def test_회원가입하면_토큰을_발급받는다(auth_api):
    결과 = auth_api.register()

    assert Status.of(결과) == Status.CREATED
    token = 결과.json()["user"]["token"]
    assert isinstance(token, str)
    assert len(token) > 0


def test_이미_사용중인_이메일로는_가입할_수_없다(auth_api):
    auth_api.register()

    결과 = auth_api.register(username="user2")  # 같은 이메일로 재가입 시도

    assert Status.of(결과) == Status.VALIDATION_ERROR


def test_비밀번호_없이는_가입할_수_없다(auth_api):
    결과 = auth_api.register(password=None)

    assert Status.of(결과) == Status.VALIDATION_ERROR


def test_username_없이는_가입할_수_없다(auth_api):
    결과 = auth_api.register(username=None)

    assert Status.of(결과) == Status.VALIDATION_ERROR