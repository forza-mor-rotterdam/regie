from __future__ import annotations

from datetime import datetime

from apps.auth.service import AuthService

TOKEN_SESSION_KEY = "msb_token"
TOKEN_SESSION_TIMESTAMP = "msb_token_timestamp"
TOKEN_EXPIRED = 1 * 60


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
        self._token = request.session.get(TOKEN_SESSION_KEY)
        self._timestamp = request.session.get(TOKEN_SESSION_TIMESTAMP)

        # request.session[TOKEN_SESSION_KEY] = self._token
        print("get token")
        print(self._token)
        print("self._timestamp")
        print(self._timestamp)
        print("datetime.timestamp(datetime.now()) + TOKEN_EXPIRED")
        print(datetime.timestamp(datetime.now()) + TOKEN_EXPIRED)
        # self._user_info = {}
        # if not token:
        self._is_authenticated = False
        if not self._token:
            return

        user_info = {}
        if self._timestamp > datetime.timestamp(datetime.now()) + TOKEN_EXPIRED:
            print("check token valid")
            user_info = AuthService().get_user_info(self._token)
        # print(self._user_info)
        if user_info.get("success"):
            self._token = None
            request.session.pop(TOKEN_SESSION_KEY)
            return
        self._is_authenticated = True

    # @property
    # def user_info(self):
    # return self._user_info

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
        request.session[TOKEN_SESSION_KEY] = token
        request.session[TOKEN_SESSION_TIMESTAMP] = datetime.timestamp(datetime.now())
        print("set token")
        print(token)
        return (True, User(request)) if success else (False, token)


authenticate = AuthenticationBackend().authenticate
