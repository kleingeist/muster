# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0007_auto_20150530_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page_height',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='page_width',
            field=models.FloatField(null=True),
        ),
    ]
