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

    patterns = page.patterns.all()
    """
    for pattern in page.patterns.all():
        bbox = dict(zip(("x", "y", "width", "height"),
                        pattern.bbox.split(" ")))
        assert len(bbox) == 4, "Invalid BBox"

        x, y, width, height = map(int, pattern.bbox.split(" "))
        shape = "{},{} {},{} {},{} {},{}".format(
            x, y,
            x + width, y,
            x + width, y + height,
            x, y + height
        )

        patterns.append({
            "id": pattern.id,
            "bbox": bbox,
            "shape": shape,
        })
    """

    context = {"page": page, "volume": volume, "patterns": patterns}
    return render(request, "musterapp/page_browser.html", context=context)

