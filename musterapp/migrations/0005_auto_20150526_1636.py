# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import musterapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0004_auto_20150526_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=musterapp.models._page_upload_to, default='', width_field='image_width', height_field='image_height', max_length=255),
        ),
    ]
