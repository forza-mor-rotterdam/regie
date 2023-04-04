from apps.services import incident_api_service


class IncidentUser:
    _is_authenticated = None
    _token = None
    _profile = None
    _request = None
    _name = None
    _email = None

    def __init__(self, request, *args, **kwargs):
        self._request = request
        token = request.session.get("token")
        self._is_authenticated = True
        self._user_info = {}
        try:
            self._user_info = incident_api_service.get_user_info(token)
        except Exception:
            self._is_authenticated = False

    @property
    def user_info(self):
        return self._user_info

    @property
    def token(self):
        return self._request.session.get("token")

    @property
    def is_authenticated(self):
        return self._is_authenticated


class IncidentAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        success, token = incident_api_service.login(
            username,
            password,
        )
        request.session["token"] = token
        return (True, IncidentUser(request)) if success else (False, token)


authenticate = IncidentAuthenticationBackend().authenticate
