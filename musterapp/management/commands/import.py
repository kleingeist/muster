import argparse

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from musterapp.models import Volume, Page, PageColor, PageType
from musterapp import helper
from django.db import connection
import os, shutil

from ._parser import MusterParser


def _set_attr(o, k, v, ignore=[]):
    if k not in ignore and k in o._meta.get_all_field_names():
        setattr(o, k, v)

class Command(BaseCommand):
    help = 'Imports the data from the XML lido file'

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', type=argparse.FileType('r'))
        parser.add_argument('imgdir', type=str)

    def handle(self, *args, **options):
        mediadir = settings.MEDIA_ROOT

        imgdir = options["imgdir"]
        if not os.path.isdir(imgdir):
            raise CommandError("imgdir has to be a directory")

        mp = MusterParser()
        metadata = mp.parse(options["xmlfile"])

        files = os.listdir(imgdir)
        files = (f for f in files if not f.startswith("."))

        double = {}
        invalid = []
        volumes = {}

        for img in files:
            try:
                (vol, p, p1, p2) = helper.img2recids(img)
            except ValueError:
                invalid.append(img)
                continue

            vid, p1id, p2id = helper.split_recid(p)

            if not vid in metadata:
                print("Volume not found: " + vol)
                continue
            vm = metadata[vid]

            if vol not in volumes:
                volumes[vol] = {
                    "record_id": vol,
                    "title": vm["title"],
                    "general_desc": vm["general_desc"],
                    "object_category": vm["object_category"],
                    "object_name": vm["object_name"],
                    "page_count": vm["page_count"],
                    "page_height": vm["page_height"],
                    "page_width": vm["page_width"],
                    "physical_desc": vm["physical_desc"],
                    "producer_location": vm["producer_location"],
                    "producer_name": vm["producer_name"],
                    "producer_role": vm["producer_role"],
                    "pages": {}
                }

            if p1id not in vm["pages"]:
                pm = {
                    "image_name": img,
                    "record_id": p,
                    "page_number": p1id,
                    "colors": [],
                    "types": [],
                    "general_desc": "",
                    "physical_desc": "",
                }
            else:
                p1m = vm["pages"][p1id]
                pm = {
                    "image_name": img,
                    "record_id": p,
                    "page_number": p1id,
                    "colors": p1m["colors"],
                    "types": p1m["types"],
                    "general_desc": p1m["general_desc"],
                    "physical_desc": p1m["physical_desc"],
                    "page_width": p1m["page_width"],
                    "page_height": p1m["page_height"],
                }

            if p2id in vm["pages"]:
                p2m = vm["pages"][p2id]

                double[p1] = double[p2] = True
                pm["colors"] = list(set(pm["colors"] + p2m["colors"]))
                pm["types"] = list(set(pm["types"] + p2m["types"]))
                pm["general_desc"] = pm["general_desc"] + "\n" + p2m["general_desc"]
                pm["physical_desc"] = pm["physical_desc"] + "\n" + p2m["physical_desc"]
                pm["page_width"] = pm["page_height"] = None

            volumes[vol]["pages"][p] = pm

        # Clear the DB
        Page.objects.all().delete()
        Volume.objects.all().delete()

        cursor = connection.cursor()
        cursor.execute('TRUNCATE TABLE "{0}", "{1}" CASCADE'.format(Page._meta.db_table, Volume._meta.db_table))

        for v in volumes.values():
            v_ = Volume()

            for k in v:
                _set_attr(v_, k, v[k], ["pages", "id"])
            v_.save()

            for p in v["pages"].values():
                if p["record_id"] in double:
                    continue

                if p["image_name"] is None:
                    print(p)
                    continue

                p_ = Page()
                for k in p:
                    _set_attr(p_, k, p[k], ["id", "types", "colors", "image"])

                # Copy the image to the media dir
                image_src = os.path.join(imgdir, p["image_name"])
                image_dst = os.path.join(mediadir, "pages", v["record_id"], p["image_name"])

                if not os.path.exists(image_dst):
                    shutil.copy(image_src, image_dst)

                image_media_path = os.path.join("pages", v["record_id"], p["image_name"])
                if image_media_path is None:
                    print("None:" + v + " - " + p)
                print(image_media_path)
                p_.image = image_media_path

                p_.volume = v_
                p_.save()

                for c in p["colors"]:
                    c_, created = PageColor.objects.get_or_create(name=c.lower())
                    if created:
                        c_.save()
                    p_.colors.add(c_)

                for t in p["types"]:
                    t_, created = PageType.objects.get_or_create(name=t.lower())
                    if created:
                        t_.save()
                    p_.types.add(t_)
