from apps.regie.views import http_404, http_500, melding_lijst, root
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("", root, name="root"),
    path("melding/", melding_lijst, name="melding_lijst"),
]


if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
