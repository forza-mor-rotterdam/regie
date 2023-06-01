from apps.meldingen.service import MeldingenService
from django.conf import settings

service_instance = MeldingenService(settings.MELDINGEN_URL)
