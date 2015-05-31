# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0006_remove_page_image_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='image_height',
            field=models.IntegerField(null=True, default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='image_width',
            field=models.IntegerField(null=True, default=0),
        ),
    ]
