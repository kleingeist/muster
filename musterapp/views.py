from django.shortcuts import render, get_object_or_404, HttpResponse
from taggit.utils import parse_tags

from .models import Page, Volume, VolumeCategory, Pattern


def index(request):
    return volume_detail(request, "HA.II.02")

def volume_detail(request, volume_rid):
    volume = get_object_or_404(Volume, record_id=volume_rid)
    pages = volume.pages.order_by("page_number").all()
    categories = VolumeCategory.objects.all().order_by("name")

    context = {"volume": volume, "pages": pages, "categories": categories}
    return render(request, "musterapp/volume_detail.html", context=context)


def page_browser(request, page_rid):
    page = get_object_or_404(Page, record_id=page_rid)
    volume = page.volume

    patterns = page.patterns.all()

    context = {"page": page, "volume": volume, "patterns": patterns}
    return render(request, "musterapp/page_browser.html", context=context)

def search(request):
    q = request.GET.get("q", "")
    tags = parse_tags(q)

    qs = Pattern.objects.all()
    for tag in tags:
        qs = qs.filter(tags__name=tag.lower())

    context = {
        "q_current": q,
        "patterns": qs.order_by("?")
    }
    return render(request, "musterapp/search.html", context=context)