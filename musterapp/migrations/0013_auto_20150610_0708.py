# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0012_auto_20150609_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pattern',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, max_length=255, null=True, width_field='image_width', upload_to='patterns/%Y/%m', height_field='image_height', default=''),
        ),
        migrations.AlterField(
            model_name='pattern',
            name='image_height',
            field=models.IntegerField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='pattern',
            name='image_width',
            field=models.IntegerField(editable=False, null=True),
        ),
    ]
