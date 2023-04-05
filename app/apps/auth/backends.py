from __future__ import annotations

from datetime import datetime

from apps.auth.service import AuthService

TOKEN_KEY = "msb_token"
TOKEN_TIMESTAMP_KEY = "msb_token_timestamp"
USER_INFO_KEY = "msb_user_info"
TOKEN_EXPIRED = 2 * 60


class User:
    _is_authenticated = None
    _token = None
    _request = None
    _name = None
    _email = None
    _token = None
    _timestamp = None

    def __init__(self, request, *args, **kwargs):
        self._request = request
        self._token = request.session.get(TOKEN_KEY)
        self._timestamp = request.session.get(TOKEN_TIMESTAMP_KEY)
        self._user_info = request.session.get(USER_INFO_KEY, {})
        self._is_authenticated = False

        if not self._token:
            return

        if self._timestamp + TOKEN_EXPIRED < datetime.timestamp(datetime.now()):
            self._user_info = AuthService().get_user_info(self._token)
            request.session[USER_INFO_KEY] = self._user_info
            request.session[TOKEN_TIMESTAMP_KEY] = datetime.timestamp(datetime.now())
        if not self.info.get("success"):
            self._token = None
            request.session.pop(TOKEN_KEY)
            return

        self._is_authenticated = True

    @property
    def info(self):
        return self._user_info

    @property
    def token(self):
        return self._token

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
        request.session[TOKEN_KEY] = token
        request.session[TOKEN_TIMESTAMP_KEY] = datetime.timestamp(datetime.now())
        request.session[USER_INFO_KEY] = AuthService().get_user_info(token)
        return (True, User(request)) if success else (False, token)


authenticate = AuthenticationBackend().authenticate
