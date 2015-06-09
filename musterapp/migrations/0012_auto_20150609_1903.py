# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0011_auto_20150609_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to='patterns/%Y/%m', max_length=255, width_field='image_width', height_field='image_height', default=''),
        ),
        migrations.AddField(
            model_name='pattern',
            name='image_height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pattern',
            name='image_width',
            field=models.IntegerField(null=True),
        ),
    ]
