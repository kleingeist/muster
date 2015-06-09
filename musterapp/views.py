from django.shortcuts import render, get_object_or_404, HttpResponse

from .models import Page, Volume, VolumeCategory


def index(request):

    categories = VolumeCategory.objects.all().order_by("name")

    context = {"categories": categories}
    return render(request, "musterapp/index.html", context=context)


def volume_detail(request, volume_rid):
    volume = get_object_or_404(Volume, record_id=volume_rid)
    pages = volume.pages.order_by("page_number").all()

    context = {"volume": volume, "pages": pages}
    return render(request, "musterapp/volume_detail.html", context=context)


def page_browser(request, page_rid):
    page = get_object_or_404(Page, record_id=page_rid)
    volume = page.volume

    context = {"page": page, "volume": volume}
    return render(request, "musterapp/page_browser.html", context=context)
