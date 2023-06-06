from urllib.parse import urlparse

import requests
from apps.meldingen.utils import get_meldingen_token
from requests import Request, Response


class MeldingenService:
    _api_base_url = None
    _timeout: tuple[int, ...] = (5, 10)
    _api_path: str = "/api/v1"

    class BasisUrlFout(Exception):
        ...

    def __init__(self, api_base_url: str, *args, **kwargs: dict):
        self._api_base_url = api_base_url.strip().rstrip("/")
        super().__init__(*args, **kwargs)

    def get_url(self, url):
        url_o = urlparse(url)
        if not url_o.scheme and not url_o.netloc:
            return f"{self._api_base_url}{url}"
        if f"{url_o.scheme}://{url_o.netloc}" == self._api_base_url:
            return url
        raise MeldingenService.BasisUrlFout(
            f"url: {url}, basis_url: {self._api_base_url}"
        )

    def get_headers(self):
        headers = {"Authorization": f"Token {get_meldingen_token()}"}
        return headers

    def do_request(self, url, method="get", data={}):

        action: Request = getattr(requests, method)
        action_params: dict = {
            "url": self.get_url(url),
            "headers": self.get_headers(),
            "json": data,
            "timeout": self._timeout,
        }
        response: Response = action(**action_params)

        return response.json()

    def get_melding_lijst(self, query_string=""):
        return self.do_request(f"{self._api_path}/melding/?{query_string}")

    def get_melding(self, id, query_string=""):
        return self.do_request(f"{self._api_path}/melding/{id}/?{query_string}")

    def melding_gebeurtenis_toevoegen(
        self,
        id,
        bijlagen=[],
        omschrijving_intern=None,
        omschrijving_extern=None,
    ):
        data = {
            "bijlagen": bijlagen,
            "omschrijving_intern": omschrijving_intern,
            "omschrijving_extern": omschrijving_extern,
        }

        return self.do_request(
            f"{self._api_path}/melding/{id}/gebeurtenis-toevoegen/",
            method="post",
            data=data,
        )

    def melding_status_aanpassen(
        self,
        id,
        status=None,
        resolutie=None,
        bijlagen=[],
        omschrijving_extern=None,
        omschrijving_intern=None,
    ):
        data = {
            "bijlagen": bijlagen,
            "omschrijving_extern": omschrijving_extern,
            "omschrijving_intern": omschrijving_intern,
        }
        if status:
            data.update(
                {
                    "status": {
                        "naam": status,
                    },
                    "resolutie": resolutie,
                }
            )
        return self.do_request(
            f"{self._api_path}/melding/{id}/status-aanpassen/"
            if status
            else f"{self._api_path}/melding/{id}/gebeurtenis-toevoegen/",
            method="patch" if status else "post",
            data=data,
        )

    def taakapplicaties(self):
        return self.do_request(f"{self._api_path}/taakapplicatie/")

    def taak_aanmaken(
        self, melding_uuid, taaktype_url, titel, bericht=None, additionele_informatie={}
    ):
        data = {
            "taaktype": taaktype_url,
            "titel": titel,
            "bericht": bericht,
            "additionele_informatie": additionele_informatie,
        }
        return self.do_request(
            f"{self._api_path}/melding/{melding_uuid}/taakopdracht/",
            method="post",
            data=data,
        )

    def taak_status_aanpassen(
        self,
        taakopdracht_url,
        status,
        resolutie=None,
        omschrijving_intern=None,
        bijlagen=None,
    ):
        data = {
            "taakstatus": {
                "naam": status,
            },
            "resolutie": resolutie,
            "omschrijving_intern": omschrijving_intern,
            "bijlagen": bijlagen,
        }
        return self.do_request(
            f"{taakopdracht_url}status-aanpassen/", method="patch", data=data
        )
