import copy
import math

import requests
import weasyprint
from apps.meldingen import service_instance
from apps.meldingen.utils import get_meldingen_token
from apps.regie.forms import (
    BEHANDEL_OPTIES,
    BEHANDEL_RESOLUTIE,
    BEHANDEL_STATUS,
    FilterForm,
    InformatieToevoegenForm,
    MeldingAfhandelenForm,
    TaakStartenForm,
)
from apps.regie.utils import to_base64
from config.context_processors import general_settings
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse, QueryDict, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
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
    standaard_waardes = {
        "ordering": "-origineel_aangemaakt",
        "offset": "0",
        "limit": "10",
    }

    query_dict = QueryDict("", mutable=True)
    query_dict.update(standaard_waardes)
    query_dict.update(request.GET)

    request.session["overview_querystring"] = request.GET.urlencode()

    data = service_instance.get_melding_lijst(query_string=query_dict.urlencode())

    pagina_aantal = math.ceil(data.get("count", 0) / int(query_dict.get("limit")))
    offset_options = [
        (str(p * int(query_dict.get("limit"))), str(p + 1))
        for p in range(0, pagina_aantal)
    ]
    query_dict["offset"] = (
        query_dict.get("offset")
        if str(query_dict.get("offset")) in [str(oo[0]) for oo in offset_options]
        else 0
    )

    locaties_geselecteerd = len(query_dict.getlist("begraafplaats"))
    begraafplaatsen = [
        [k, f"{v[0]}"]
        for k, v in data.get("filter_options", {}).get("begraafplaats", {}).items()
    ]
    form = FilterForm(
        query_dict, offset_options=offset_options, locatie_opties=begraafplaatsen
    )
    filter_form_data = copy.deepcopy(standaard_waardes)
    if form.is_valid():
        filter_form_data = copy.deepcopy(form.cleaned_data)
    limit = int(filter_form_data.get("limit", "10"))
    offset = int(filter_form_data.get("offset", "0"))
    ordering = filter_form_data.get("ordering")

    meldingen = data.get("results", [])
    totaal = data.get("count", 0)
    pageNumTotal = int(
        (totaal - (totaal % limit)) / limit + (1 if totaal % limit > 0 else 0)
    )
    pages = []
    for pageNum in range(pageNumTotal):
        pages.append(f"limit={limit}&offset={pageNum * limit}&ordering={ordering}")
    currentPage = offset / limit + 1
    volgende = data.get("next")
    vorige = data.get("previous")
    startNum = int((currentPage - 1) * limit)
    endNum = int(min([currentPage * limit, totaal]))
    melding_aanmaken_url = settings.MELDING_AANMAKEN_URL

    return render(
        request,
        "melding/part_overview_table.html",
        {
            "meldingen": meldingen,
            "totaal": totaal,
            "volgende": volgende,
            "vorige": vorige,
            "startNum": startNum,
            "endNum": endNum,
            "form": form,
            "locaties_geselecteerd": locaties_geselecteerd,
            "filter_options": data.get("filter_options", {}),
            "melding_aanmaken_url": melding_aanmaken_url,
        },
    )


def detail(request, id):
    melding = service_instance.get_melding(id)
    melding_gebeurtenissen = melding["melding_gebeurtenissen"]
    bijlagen_extra = []
    for b in melding_gebeurtenissen:
        if len(b["bijlagen"]) > 0:
            for f in b["bijlagen"]:
                bijlagen_extra.append(f)
    form = InformatieToevoegenForm()
    overview_querystring = request.session.get("overview_querystring", "")
    if request.POST:
        form = InformatieToevoegenForm(request.POST)
        if form.is_valid():
            bijlagen = request.FILES.getlist("bijlagen", [])
            bijlagen_base64 = []
            for f in bijlagen:
                file_name = default_storage.save(f.name, f)
                bijlagen_base64.append({"bestand": to_base64(file_name)})

            response_melding = service_instance.melding_status_aanpassen(
                id,
                omschrijving_intern=form.cleaned_data.get("omschrijving_intern"),
                bijlagen=bijlagen_base64,
            )
            print(response_melding)
            return redirect("detail", id=id)

    return render(
        request,
        "melding/part_detail.html",
        {
            "melding": melding,
            "form": form,
            "overview_querystring": overview_querystring,
            "bijlagen_extra": bijlagen_extra,
        },
    )


def melding_afhandelen(request, id):
    melding = service_instance.get_melding(id)
    afhandel_reden_opties = [(s, s) for s in melding.get("volgende_statussen", ())]
    form = MeldingAfhandelenForm()
    if request.POST:
        form = MeldingAfhandelenForm(request.POST)
        if form.is_valid():
            bijlagen = request.FILES.getlist("bijlagen", [])
            bijlagen_base64 = []
            for f in bijlagen:
                file_name = default_storage.save(f.name, f)
                bijlagen_base64.append({"bestand": to_base64(file_name)})

            response_melding = service_instance.melding_status_aanpassen(
                id,
                status=BEHANDEL_STATUS.get(form.cleaned_data.get("status")),
                resolutie=BEHANDEL_RESOLUTIE.get(form.cleaned_data.get("status")),
                omschrijving_extern=form.cleaned_data.get("omschrijving_extern"),
                omschrijving_intern=form.cleaned_data.get("omschrijving_intern"),
                bijlagen=bijlagen_base64,
            )
            print(response_melding)
            return redirect("detail", id=id)

    return render(
        request,
        "melding/part_melding_afhandelen.html",
        {
            "form": form,
            "melding": melding,
            "afhandel_reden_opties": afhandel_reden_opties,
            "standaard_afhandel_teksten": {bo[0]: bo[2] for bo in BEHANDEL_OPTIES},
        },
    )


def taak_starten(request, id):
    melding = service_instance.get_melding(id)
    form = TaakStartenForm()
    if request.POST:
        form = TaakStartenForm(request.POST)
        if form.is_valid():

            response_melding = service_instance.melding_status_aanpassen(
                id,
                status=BEHANDEL_STATUS.get(form.cleaned_data.get("status")),
                resolutie=BEHANDEL_RESOLUTIE.get(form.cleaned_data.get("status")),
                omschrijving_extern=form.cleaned_data.get("omschrijving_extern"),
                omschrijving_intern=form.cleaned_data.get("omschrijving_intern"),
            )
            print(response_melding)
            return redirect("detail", id=id)

    return render(
        request,
        "melding/part_taak_starten.html",
        {
            "form": form,
            "melding": melding,
        },
    )


def informatie_toevoegen(request, id):
    melding = service_instance.get_melding(id)
    form = InformatieToevoegenForm()
    if request.POST:
        form = InformatieToevoegenForm(request.POST)
        if form.is_valid():
            bijlagen = request.FILES.getlist("bijlagen_extra", [])
            bijlagen_base64 = []
            for f in bijlagen:
                file_name = default_storage.save(f.name, f)
                bijlagen_base64.append({"bestand": to_base64(file_name)})

            response_melding = service_instance.melding_status_aanpassen(
                id,
                omschrijving_intern=form.cleaned_data.get("opmerking"),
                bijlagen=bijlagen_base64,
            )
            print(response_melding)
            return redirect("detail", id=id)

    return render(
        request,
        "melding/part_informatie_toevoegen.html",
        {
            "melding": melding,
            "form": form,
        },
    )


def root(request):
    return redirect(reverse("melding_lijst"))


def melding_lijst(request):

    return render(
        request,
        "melding/index.html",
        {
            # "meldingen": alle_meldingen,
        },
    )


def melding_pdf_download(request, id):
    melding = service_instance.get_melding(id)
    base_url = request.build_absolute_uri()
    path_to_css_file = (
        "/app/frontend/public/build/app.css" if settings.DEBUG else "/static/app.css"
    )
    context = {
        "melding": melding,
        "base_url": f"{request.scheme}://{request.get_host()}",
    }
    context.update(general_settings(request))

    html = render_to_string("pdf/melding.html", context=context)

    pdf = weasyprint.HTML(string=html, base_url=base_url).write_pdf(
        stylesheets=[path_to_css_file]
    )
    pdf_filename = f"serviceverzoek_{id}.pdf"

    return HttpResponse(
        pdf,
        content_type="application/pdf",
        headers={"Content-Disposition": f'attachment;filename="{pdf_filename}"'},
    )


def meldingen_bestand(request):
    url = f"{settings.MELDINGEN_URL}{request.path}"
    headers = {"Authorization": f"Token {get_meldingen_token()}"}
    response = requests.get(url, stream=True, headers=headers)
    return StreamingHttpResponse(
        response.raw,
        content_type=response.headers.get("content-type"),
        status=response.status_code,
        reason=response.reason,
    )


def gebruiker_informatie(request):
    return render(
        request,
        "auth/gebruiker_informatie.html",
    )


@login_required
def login_verplicht(request):
    return render(
        request,
        "auth/login_verplicht.html",
    )


def login_mislukt(request):
    return render(
        request,
        "auth/login_mislukt.html",
    )
