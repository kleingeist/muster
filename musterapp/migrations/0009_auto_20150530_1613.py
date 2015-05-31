# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0008_auto_20150530_1603'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='number',
            new_name='page_number',
        ),
        migrations.RemoveField(
            model_name='page',
            name='object_category',
        ),
        migrations.RemoveField(
            model_name='page',
            name='object_name',
        ),
    ]
