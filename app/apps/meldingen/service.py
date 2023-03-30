import requests
from requests import Request, Response


class MeldingenService:
    _api_base_url = None
    _timeout: tuple[int, ...] = (5, 10)

    def __init__(self, api_base_url: str, *args, **kwargs: dict):
        self._api_base_url = api_base_url.strip().rstrip("/")
        super().__init__(*args, **kwargs)

    def get_url(self, url):
        return f"{self._api_base_url}{url}"

    def do_request(self, url, method="get", data={}):

        action: Request = getattr(requests, method)
        action_params: dict = {
            "url": self.get_url(url),
            "headers": {},
            "json": data,
            "timeout": self._timeout,
        }
        response: Response = action(**action_params)
        return response.json()

    def get_melding_lijst(self, query_string=""):
        return self.do_request(f"/melding/?{query_string}")

    def get_melding(self, id, query_string=""):
        return self.do_request(f"/melding/{id}/?{query_string}")
