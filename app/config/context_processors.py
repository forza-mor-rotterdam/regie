from django.conf import settings


def general_settings(context):
    return {
        "DEBUG": settings.DEBUG,
        "DEV_SOCKET_PORT": settings.DEV_SOCKET_PORT,
        "MELDINGEN_URL": settings.MELDINGEN_URL,
    }
