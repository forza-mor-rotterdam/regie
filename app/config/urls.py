from apps.regie.views import (
    detail,
    gebruiker_informatie,
    http_404,
    http_500,
    informatie_toevoegen,
    login_mislukt,
    login_verplicht,
    melding_afhandelen,
    melding_lijst,
    melding_pdf_download,
    meldingen_bestand,
    overview,
    root,
    sso_logout,
    taak_afronden,
    taak_starten,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.authtoken import views

urlpatterns = [
    path("", root, name="root"),
    path("api-token-auth/", views.obtain_auth_token),
    path("melding/", melding_lijst, name="melding_lijst"),
    path("health/", include("health_check.urls")),
    path("part/melding/", overview, name="overview"),
    path(
        "part/melding/<uuid:id>/afhandelen/",
        melding_afhandelen,
        name="melding_afhandelen",
    ),
    path(
        "part/melding/<uuid:id>/taakstarten/",
        taak_starten,
        name="taak_starten",
    ),
    path(
        "part/melding/<uuid:melding_uuid>/taak-afronden/<uuid:taakopdracht_uuid>/",
        taak_afronden,
        name="taak_afronden",
    ),
    path(
        "part/melding/<uuid:id>/informatie-toevoegen/",
        informatie_toevoegen,
        name="informatie_toevoegen",
    ),
    path("melding/<uuid:id>", detail, name="detail"),
    path(
        "download/melding/<uuid:id>/pdf/",
        melding_pdf_download,
        name="melding_pdf_download",
    ),
    path("admin/", admin.site.urls),
    re_path(r"media/", meldingen_bestand, name="meldingen_bestand"),
]

if settings.OIDC_RP_CLIENT_ID:
    urlpatterns += [
        path(
            "gebruiker-informatie/", gebruiker_informatie, name="gebruiker_informatie"
        ),
        path("login-verplicht/", login_verplicht, name="login_verplicht"),
        path("login-mislukt/", login_mislukt, name="login_mislukt"),
        path("sso-logout/", sso_logout, name="sso_logout"),
        path("oidc/", include("mozilla_django_oidc.urls")),
    ]


if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
