from .models import Volume

def volume_menu(request):
    record_ids = Volume.objects.order_by("record_id").values_list("record_id",
                                                                  flat=True)

    return {"menu": {"volumes": record_ids}}


from taggit.models import Tag
def tag_list_all(request):
    tags = Tag.objects.all().values_list("name", flat=True)
    return {"tag_list_all": tags}