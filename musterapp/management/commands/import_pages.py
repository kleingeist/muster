import argparse
import os
from os import path
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from musterapp.models import Volume, Vector, Page, PageColor, PageType, VolumeCategory, Pattern
from musterapp import helper
from ._parser import MusterParser
from sorl.thumbnail.fields import ImageField
from django.db.models.fields.files import ImageFieldFile
import json



class Command(BaseCommand):
    help = 'Imports the pages kind of'

    def add_arguments(self, parser):
        parser.add_argument("volumes", type=str, nargs="+")

    def handle(self, *args, **options):
        mediadir = settings.MEDIA_ROOT

        for vol_id in options["volumes"]:
            volume = Volume.objects.get(record_id=vol_id)

            for page in volume.pages.all():
                img_name = helper.recid2img(page.record_id, "png")
                img_path = os.path.join("pages", vol_id, img_name)
                img_abs = os.path.join(mediadir, img_path)
                if os.path.isfile(img_abs):
                    page.image = img_path
                    page.save()
