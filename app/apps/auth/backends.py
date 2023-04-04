from __future__ import annotations

from apps.auth.service import AuthService


class User:
    _is_authenticated = None
    _token = None
    _request = None
    _name = None
    _email = None

    def __init__(self, request, *args, **kwargs):
        self._request = request
        token = request.session.get("token")
        self._is_authenticated = True
        self._user_info = {}
        self._user_info = AuthService().get_user_info(token)
        self._is_authenticated = False
        if self._user_info.get("success"):
            self._is_authenticated = True

    @property
    def user_info(self):
        return self._user_info

    @property
    def token(self):
        return self._request.session.get("token")

    @property
    def is_authenticated(self):
        return self._is_authenticated


class AuthenticationBackend:
    def authenticate(
        self, request, username: str | None = None, password: str | None = None
    ):
        success, token = AuthService().login(
            username,
            password,
        )
        request.session["token"] = token
        return (True, User(request)) if success else (False, token)


authenticate = AuthenticationBackend().authenticate
