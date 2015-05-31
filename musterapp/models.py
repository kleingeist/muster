from django.db import models
from sorl.thumbnail import ImageField

class Volume(models.Model):
    record_id = models.CharField(max_length=32, unique=True)

    title = models.CharField(max_length=255)
    object_name = models.CharField(max_length=255)
    object_category = models.CharField(max_length=255)

    general_desc = models.TextField(blank=True)
    physical_desc = models.TextField(blank=True)

    page_width = models.FloatField()
    page_height = models.FloatField()

    producer_name = models.CharField(max_length=255, blank=True)
    producer_role = models.CharField(max_length=255, blank=True)
    producer_location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.record_id

    def first_page(self):
        return self.pages.order_by('page_number').first()


def _page_upload_to(page, filename):
    if page.record_id and len(page.record_id) > 8:
        return "pages/" + page.record_id[:8] + "/" + page.record_id[8:]
    else:
        return "pages/unsorted"

class Page(models.Model):
    volume = models.ForeignKey(Volume, related_name="pages")

    record_id = models.CharField(max_length=32, unique=True)
    page_number = models.SmallIntegerField(default=-1)

    image_name = models.CharField(max_length=255)
    image = ImageField(upload_to=_page_upload_to, default='', max_length=255,
                       height_field="image_height", width_field="image_width")
    image_height = models.IntegerField(default=0, null=True)
    image_width = models.IntegerField(default=0, null=True)

    general_desc = models.TextField(blank=True)
    physical_desc = models.TextField(blank=True)

    page_width = models.FloatField(null=True)
    page_height = models.FloatField(null=True)

    colors = models.ManyToManyField("PageColor")
    types = models.ManyToManyField("PageType")

    def __str__(self):
        return self.record_id

    def next_page(self):
        return self.volume.pages.filter(
            page_number__gt=self.page_number).order_by('page_number').first()

    def prev_page(self):
        return self.volume.pages.filter(
            page_number__lt=self.page_number).order_by('-page_number').first()


class PageColor(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self): 
        return self.name

class PageType(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self): 
        return self.name


