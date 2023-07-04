from apps.meldingen.utils import get_meldingen_token
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import HealthCheckException


class MeldingenTokenCheck(BaseHealthCheckBackend):
    critical_service = False

    def check_status(self):
        try:
            get_meldingen_token()
            return "OK"
        except Exception as e:
            raise HealthCheckException(e)

    def identifier(self):
        return self.__class__.__name__
