import weasyprint
from apps.meldingen import service_instance
from apps.regie.mock import meldingen
from config.context_processors import general_settings
from django.conf import settings
from django.http import HttpResponse
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
    ordering = request.GET.get("ordering", "aangemaakt_op")
    offset = request.GET.get("offset", "0")
    limit = request.GET.get("limit", "5")
    data = service_instance.get_melding_lijst(
        query_string=f"limit={limit}&offset={offset}&ordering={ordering}"
    )
    meldingen = data.get("results", [])
    totaal = data.get("count", 0)
    offset = int(offset)
    limit = int(limit)
    pageNumTotal = int(
        (totaal - (totaal % limit)) / limit + (1 if totaal % limit > 0 else 0)
    )
    pages = []
    for pageNum in range(pageNumTotal):
        pages.append(f"limit={limit}&offset={pageNum * limit}&ordering={ordering}")
    currentPage = offset / limit + 1
    volgende = data.get("next")
    vorige = data.get("previous")
    offsetVolgende = offset + limit
    offsetVorige = offset - limit
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
            "offsetVolgende": offsetVolgende,
            "offsetVorige": offsetVorige,
            "offset": offset,
            "limit": limit,
            "pages": pages,
            "currentPage": currentPage,
            "startNum": startNum,
            "endNum": endNum,
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
    ordering = request.GET.get("ordering", "aangemaakt_op")
    try:
        data = service_instance.get_melding_lijst(query_string=f"ordering={ordering}")
        alle_meldingen = data.get("results", [])

    except Exception:
        alle_meldingen = meldingen

    return render(
        request,
        "melding/index.html",
        {
            "meldingen": alle_meldingen,
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
