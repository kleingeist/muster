from django.shortcuts import render, Http404

from .models import Page, Volume

def index(request):
    volumes = Volume.objects.all().order_by("record_id")

    context = {"volumes": volumes}
    return render(request, "musterapp/index.html", context=context)


def volume_list(request, volume_rid, page_number=1):
    volume = Volume.objects.get(record_id=volume_rid)

    page_number = int(page_number)
    if page_number % 2 > 0:
        left_number = page_number - 1
    else:
        left_number = page_number

    right_number = left_number + 1

    pages = volume.pages.filter(
        number__in=[left_number, right_number]).order_by("number")

    if len(pages) > 1:
        left = pages[0]
        right = pages[1]
    elif pages and left_number == pages[0].number:
        left = pages[0]
        right = None
    elif pages and right_number == pages[0].number:
        left = None
        right = pages[0]
    else:
        raise Http404("Invalid page number")

    context = {"volume": volume, "page_left": left, "page_right": right,
               "prev_page_number": left_number - 1 if left_number > 0 else 0,
               "next_page_number": right_number + 1}
    return render(request, "musterapp/volume_list.html", context=context)