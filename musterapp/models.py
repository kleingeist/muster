from django.db import models
from django.conf import settings
from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager

from .fields import BBoxField


class VolumeCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255)

    color = models.CharField(max_length=8)

    def __str__(self):
        return self.name

    def volumes_ordered(self):
        return self.volumes.all().order_by("record_id")


class Volume(models.Model):
    record_id = models.CharField(max_length=32, unique=True)

    title = models.CharField(max_length=255)
    category = models.ForeignKey(VolumeCategory, related_name="volumes")

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

    def preview_page(self):
        return self.pages.order_by('page_number').first()

    def page_record_ids(self):
        return self.pages.values_list('record_id', flat=True)\
            .order_by('page_number')


def _page_upload_to(page, filename):
    if page.record_id and len(page.record_id) >= 8:
        return "pages/{}/{}".format(page.record_id[:8], filename)
    return "pages/unsorted/{}".format(filename)


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

    def vectorized_patterns(self):
        return self.patterns.filter(vectors__isnull=False)


class PageColor(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self): 
        return self.name


class PageType(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self): 
        return self.name


def _pattern_upload_to(pattern, filename):
    if pattern.page and pattern.page.record_id:
        return "patterns/{}/{}".format(pattern.page.record_id, filename)
    return "patterns/unsorted/{}".format(filename)


class Pattern(models.Model):
    page = models.ForeignKey(Page, related_name="patterns")

    bbox = BBoxField()
    shape = models.TextField(blank=True)

    image = ImageField(upload_to=_pattern_upload_to, default='', max_length=255,
                       height_field="image_height", width_field="image_width",
                       blank=True, null=True)
    image_height = models.IntegerField(null=True, editable=False)
    image_width = models.IntegerField(null=True, editable=False)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return "{}:{}".format(self.page, self.id)


class Vector(models.Model):
    pattern = models.ForeignKey(Pattern, related_name="vectors")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    file = models.FileField(upload_to="vectors/%Y/%m", default=None,
                            max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}/{}".format(self.pattern, self.id)
