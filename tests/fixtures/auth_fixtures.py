"""Auth fixtures for tests"""

import pytest

# 기본 유저 정보
DEFAULT_EMAIL = "test@example.com"
DEFAULT_PASSWORD = "password123"
DEFAULT_USERNAME = "testuser"


class AuthAPI:
    """Auth API 헬퍼 클래스"""

    def __init__(self, client, token=None):
        self._client = client
        self.token = token

    def _get_headers(self):
        if self.token:
            return {"Authorization": f"Token {self.token}"}
        return None

    def register(self, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD, username=DEFAULT_USERNAME):
        """회원가입"""
        user_data = {}
        if email is not None:
            user_data["email"] = email
        if password is not None:
            user_data["password"] = password
        if username is not None:
            user_data["username"] = username

        response = self._client.post("/users", json={"user": user_data})
        if response.status_code == 201:
            self.token = response.json()["user"]["token"]
        return response

    def login(self, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD):
        """로그인"""
        payload = {"user": {
                            "email": email, 
                            "password": password
                            }
                   }
        response = self._client.post("/users/login", json=payload)
        if response.status_code == 200:
            self.token = response.json()["user"]["token"]
        return response

    def userinfo(self):
        """현재 유저 정보 조회"""
        return self._client.get("/user", headers=self._get_headers())

    def update(self, **fields):
        """유저 정보 수정"""
        payload = {"user": fields}
        return self._client.put("/user", json=payload, headers=self._get_headers())

    # Profile
    def get_profile(self, username):
        """프로필 조회"""
        return self._client.get(f"/profiles/{username}", headers=self._get_headers())

    def follow(self, username):
        """팔로우"""
        return self._client.post(f"/profiles/{username}/follow", headers=self._get_headers())

    def unfollow(self, username):
        """언팔로우"""
        return self._client.delete(f"/profiles/{username}/follow", headers=self._get_headers())


@pytest.fixture
def auth_api(client):
    """AuthAPI 인스턴스 반환"""
    return AuthAPI(client)

