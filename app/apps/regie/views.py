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


def overview(request):
    ordering = request.GET.get("ordering", "aangemaakt_op")
    try:
        alle_meldingen = service_instance.get_melding_lijst(
            query_string=f"ordering={ordering}"
        ).get("results", [])
        # alle_meldingen_gesorteerd = sort_function.get(sort_by, sort_function[DAYS])[0]
    except Exception:
        # print(e)
        alle_meldingen = meldingen
    # print(alle_meldingen)

    return render(
        request,
        "melding/part_overview_table.html",
        {
            "meldingen": alle_meldingen,
        },
    )


def root(request):
    return redirect(reverse("melding_lijst"))


def melding_lijst(request):
    ordering = request.GET.get("ordering", "aangemaakt_op")
    try:
        alle_meldingen = service_instance.get_melding_lijst(
            query_string=f"ordering={ordering}"
        ).get("results", [])
        # alle_meldingen_gesorteerd = sort_function.get(sort_by, sort_function[DAYS])[0]
    except Exception:
        # print(e)
        alle_meldingen = meldingen
    # print(alle_meldingen)

    return render(
        request,
        "melding/index.html",
        {
            "meldingen": alle_meldingen,
        },
    )
