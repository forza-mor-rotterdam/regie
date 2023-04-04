from __future__ import annotations

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from requests import Request, Response


def import_from_settings(attr, *args):
    """
    Load an attribute from the django settings.
    :raises:
        ImproperlyConfigured
    """
    try:
        if args:
            return getattr(settings, attr, args[0])
        return getattr(settings, attr)
    except AttributeError:
        raise ImproperlyConfigured("Setting {0} not found".format(attr))


class AuthService:
    _api_base_url = None
    _timeout: tuple[int, ...] = (5, 10)

    def __init__(self, *args, **kwargs: dict):
        self.MSB_AUTHORIZATION_ENDPOINT = self.get_settings(
            "MSB_AUTHORIZATION_ENDPOINT"
        )
        super().__init__(*args, **kwargs)

    def get_url(self, url):
        return f"{self.MSB_AUTHORIZATION_ENDPOINT}{url}"

    @staticmethod
    def get_settings(attr, *args):
        return import_from_settings(attr, *args)

    def do_request(self, url, user_token=None, method="get", data={}):
        headers = {}
        if user_token is not None:
            headers.update({"Authorization": f"Bearer {user_token}"})

        action: Request = getattr(requests, method)
        url = self.get_url(url)
        print(url)
        action_params: dict = {
            "url": self.get_url(url),
            "headers": headers,
            "data": data,
            "timeout": self._timeout,
        }
        response: Response = action(**action_params)
        print(response.status_code)
        print(response.text)
        return response.json()

    def get_user_info(self, user_token):
        return self.do_request("/gebruikerinfo", user_token)

    def login(self, username: str, password: str):
        data = {
            "uid": username,
            "pwd": password,
        }
        response_data = self.do_request(
            "/login",
            user_token=None,
            method="post",
            data=data,
        )
        print(response_data)
        return bool(response_data.get("success")), response_data.get("result")
