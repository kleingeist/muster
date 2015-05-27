# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import musterapp.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0002_auto_20150526_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='image',
            field=sorl.thumbnail.fields.ImageField(height_field='img_height', max_length=255, upload_to=musterapp.models._page_upload_to, default='', width_field='img_width'),
        ),
    ]
