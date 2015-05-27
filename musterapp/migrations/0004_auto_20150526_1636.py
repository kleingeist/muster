# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0003_auto_20150526_1618'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='img_height',
            new_name='image_height',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='img_name',
            new_name='image_name',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='img_width',
            new_name='image_width',
        ),
    ]
