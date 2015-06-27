import re
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from taggit.utils import parse_tags

from .models import *
from .forms import VectorForm
from favit.models import Favorite



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

    favorites = {}
    if request.user.is_authenticated():
        user_favs = Favorite.objects.for_user(request.user, Pattern).filter(target_object_id__in=patterns)
        favorites = {fav.target_object_id: True for fav in user_favs}

    context = {"page": page,
               "volume": volume,
               "patterns": patterns,
               "favorites": favorites}
    return render(request, "musterapp/page_browser.html", context=context)


def search(request):
    q = request.GET.get("q", "")
    faved = bool(request.GET.get("faved", False))
    tags = parse_tags(q)

    patterns = Pattern.objects.all().order_by("?")
    for tag in tags:
        patterns = patterns.filter(tags__name=tag.lower())

    favorites = {}
    if request.user.is_authenticated():
        user_favs = Favorite.objects.for_user(request.user, Pattern).values_list("target_object_id", flat=True)
        favorites = {fav_id: True for fav_id in user_favs}

        if faved:
            patterns = patterns.filter(id__in=user_favs)

    paginator = Paginator(patterns, 12)
    page = request.GET.get('page')
    try:
        patterns = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        patterns = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        patterns = paginator.page(paginator.num_pages)

    context = {
        "q_current": q,
        "faved": faved,
        "favorites": favorites,
        "patterns": patterns
    }
    return render(request, "musterapp/search.html", context=context)


def pattern_detail(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id)
    vectors = pattern.vectors.all()
    page = pattern.page
    tags = pattern.tags.all()

    if request.method == 'POST' and request.user.is_authenticated():
        form = VectorForm(request.POST, request.FILES)
        issvg = request.FILES['vectorfile'].content_type == 'image/svg+xml'

        if form.is_valid() and issvg:
            newvector = Vector(pattern=pattern,
                               file=request.FILES['vectorfile'],
                               author=request.user)
            newvector.save()

            return redirect('musterapp.views.pattern_detail', pattern_id)
    else:
        form = VectorForm()

    favorites = {}
    if request.user.is_authenticated():
        fav = Favorite.objects.get_favorite(request.user, pattern, Pattern)
        favorites[pattern.id] = (fav is not None)

    context = {
        "pattern": pattern,
        "page": page,
        "favorites": favorites,
        "vectors": vectors,
        "tags": tags,
        "form": form
    }
    return render(request, "musterapp/pattern_detail.html", context=context)

@require_POST
def add_tag(request, pattern_id):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    tag = request.POST.get("tag", "")
    if not re.match(r'^[-\w]+$', tag):
        return HttpResponseBadRequest()

    pattern = get_object_or_404(Pattern, id=pattern_id)
    exists = pattern.tags.filter(name=tag).exists()

    if not exists:
        pattern.tags.add(tag)

    from .templatetags.tag_colors import as_taga
    data = {
        "created": not exists,
        "tag": tag,
        "html": str(as_taga(tag))
    }
    return JsonResponse(data)


@require_POST
def rate_vector(request, vector_id):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    rating = int(request.REQUEST.get("rating", -1))

    if not (0 <= rating <= 5):
        return HttpResponseBadRequest()

    vector = get_object_or_404(Vector, id=vector_id)

    try:
        vector_rating = VectorRating.objects.get(vector=vector, user=request.user)
        created = False
    except ObjectDoesNotExist:
        vector_rating = VectorRating(vector=vector, user=request.user)
        created = True

    #vector_rating, created = VectorRating.objects.get_or_create(vector=vector, user=request.user)
    vector_rating.rating = rating
    vector_rating.save()

    data = {
        "created": created,
        "rating": vector_rating.vector.rating
    }
    return JsonResponse(data)
