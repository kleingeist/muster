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



def _set_attr(o, k, v, ignore=[]):
    if k not in ignore and k in o._meta.get_all_field_names():
        setattr(o, k, v)

class Command(BaseCommand):
    help = 'Imports the pattern data from the XML lido file'

    def add_arguments(self, parser):
        parser.add_argument("page_name", type=str)
        parser.add_argument('imgdir', type=str)

    def handle(self, *args, **options):
        mediadir = settings.MEDIA_ROOT

        imgdir = options["imgdir"]
        if not os.path.isdir(imgdir):
            raise CommandError("imgdir has to be a directory")

        vid, cid, p1id, p2id = helper.img2recids(options["page_name"])

        page = Page.objects.get(record_id=cid)
        if page is None:
            raise CommandError("Unknown page record id " + cid)

        img_name = helper.recid2img(cid, ext="png")
        page_src = path.join(imgdir, "edited_scans", img_name)
        if not os.path.exists(page_src):
            raise CommandError("Wrong img " + page_src)

        page_dst = os.path.join(mediadir, "pages", "cropped")
        if not os.path.isdir(page_dst):
            os.makedirs(page_dst)
        page_dst = path.join(page_dst, img_name)
        shutil.copy(page_src, page_dst)

        page.image = "pages/cropped/" + img_name
        page.save()

        dir_name = img_name[:-4]
        dir_src = path.join(imgdir, "edited_crops", dir_name)
        dir_dst = path.join(mediadir, "patterns", dir_name)
        if not os.path.isdir(dir_dst):
            os.makedirs(dir_dst)

        vector_dst = path.join(mediadir, "vectors", dir_name)
        if not os.path.isdir(vector_dst):
            os.makedirs(vector_dst)

        with open(path.join(imgdir, "edited_scans",
                            helper.recid2img(cid, ext="txt"))) as f:
            pos = json.load(f)

        Pattern.objects.filter(page=page).delete()

        for i, start in enumerate(pos["start_pos"]):
            img_name = str(i) + ".png"
            vec_name = str(i) + ".svg"

            shutil.copy(path.join(dir_src, img_name),
                        path.join(dir_dst, img_name))
            shutil.copy(path.join(dir_src, vec_name),
                        path.join(vector_dst, vec_name))

            pattern = Pattern()

            pattern.page = page
            pattern.image = "patterns/" + dir_name + "/" + img_name
            bbox = {
                "x": start[0],
                "y": start[1],
                "width":  pos["width"],
                "height": pos["height"]
            }
            pattern.bbox = bbox
            pattern.save()

            vector = Vector()

            vector.pattern = pattern
            vector.file = "vectors/" + dir_name + "/" + vec_name
            vector.save()
