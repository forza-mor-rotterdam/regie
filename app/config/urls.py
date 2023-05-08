from apps.regie.views import (
    detail,
    gebruiker_informatie,
    http_404,
    http_500,
    login_mislukt,
    login_verplicht,
    melding_lijst,
    melding_pdf_download,
    meldingen_bestand,
    overview,
    root,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("", root, name="root"),
    path("melding/", melding_lijst, name="melding_lijst"),
    path("health/", include("health_check.urls")),
    path("part/melding/", overview, name="overview_part"),
    path("part/detail/<int:id>", detail, name="detail_part"),
    path(
        "download/melding/<int:id>/pdf/",
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
        path("oidc/", include("mozilla_django_oidc.urls")),
    ]


if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
