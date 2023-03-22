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
    return render(
        request,
        "melding/index.html",
        {},
    )
