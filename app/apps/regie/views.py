from apps.meldingen import service_instance
from apps.regie.mock import meldingen
from django.shortcuts import redirect, render
from django.urls import reverse


def http_404(request):
    return render(
        request,
        "404.html",
    )


def http_500(request):
    return render(
        request,
        "500.html",
    )


def root(request):
    return redirect(reverse("melding_lijst"))


def melding_lijst(request):
    try:
        alle_meldingen = service_instance.get_melding_lijst().get("results", [])
    except Exception as e:
        print(e)
        alle_meldingen = meldingen
    print(alle_meldingen)

    return render(
        request,
        "melding/index.html",
        {
            "meldingen": alle_meldingen,
        },
    )
