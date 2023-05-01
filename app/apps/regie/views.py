import copy
import math

import weasyprint
from apps.meldingen import service_instance
from apps.regie.forms import FilterForm
from config.context_processors import general_settings
from django.conf import settings
from django.http import HttpResponse, QueryDict
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

    query_dict_vorige = request.session.get("meldingen_query_params")
    print(query_dict_vorige)
    query_dict_vorige.pop("ordering")
    query_dict_vorige.pop("offset")
    query_dict_vorige.pop("limit")

    standaard_waardes = {
        "ordering": "aangemaakt_op",
        "offset": "0",
        "limit": "10",
    }

    query_dict = QueryDict("", mutable=True)
    query_dict.update(standaard_waardes)

    query_dict.update(request.GET)

    query_dict_kopie = QueryDict("", mutable=True)
    query_dict_kopie.update(query_dict)
    query_dict_kopie.pop("ordering")
    query_dict_kopie.pop("offset")
    query_dict_kopie.pop("limit")
    print(query_dict_vorige)
    print(query_dict_kopie)

    if query_dict_kopie != query_dict_vorige:
        query_dict.update(
            {"offset": standaard_waardes["offset"], "limit": standaard_waardes["limit"]}
        )

    data = service_instance.get_melding_lijst(query_string=query_dict.urlencode())

    pagina_aantal = math.ceil(data.get("count", 0) / int(query_dict.get("limit")))
    offset_options = [
        (str(p * int(query_dict.get("limit"))), str(p + 1))
        for p in range(0, pagina_aantal)
    ]

    # query_dict["offset"] = (
    #     query_dict.get("offset")
    #     if str(query_dict.get("offset")) in [str(oo[0]) for oo in offset_options]
    #     else 0
    # )

    if str(query_dict.get("offset")) not in [str(oo[0]) for oo in offset_options]:
        query_dict.update({"offset": standaard_waardes["offset"]})
        data = service_instance.get_melding_lijst(query_string=query_dict.urlencode())

    request.session["meldingen_query_params"] = query_dict

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
            "query_string": query_dict.urlencode(),
        },
    )


def detail(request, id):
    melding = service_instance.get_melding(id)
    return render(
        request,
        "melding/part_detail.html",
        {
            "melding": melding,
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
