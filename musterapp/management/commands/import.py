import argparse

from django.core.management.base import BaseCommand, CommandError
from musterapp.models import Volume, Page, PageColor, PageType
from django.db import connection

from ._parser import MusterParser

def _set_attr(o, k, v, ignore=[]):
    if k not in ignore and k in o._meta.get_all_field_names():
        setattr(o, k, v)

class Command(BaseCommand):
    help = 'Imports the data from the XML lido file'

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', type=argparse.FileType('r'))
        parser.add_argument('--cachedir', default=None)

    def handle(self, *args, **options):
        cachedir = options["cachedir"]

        mp = MusterParser(cachedir)
        data = mp.parse(options["xmlfile"])

        data = {2: data[2]}

        Page.objects.all().delete()
        Volume.objects.all().delete()

        cursor = connection.cursor()
        cursor.execute('TRUNCATE TABLE "{0}", "{1}" CASCADE'.format(Page._meta.db_table, Volume._meta.db_table))


        for v in data.values():
            v_ = Volume()

            for k in v:
                _set_attr(v_, k, v[k], ["pages", "id"])
            v_.save()


            for n, p in v["pages"].items():
                p_ = Page()
                for k in p:
                    _set_attr(p_, k, p[k], ["id", "number", "types", "colors"])

                p_.number = n
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


        #
        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write('Successfully closed poll "%s"' % poll_id)
