# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import musterapp.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='image_meta',
            field=models.FileField(max_length=255, upload_to=musterapp.models._page_upload_to, default=''),
        ),
        migrations.AddField(
            model_name='page',
            name='img_height',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='page',
            name='img_width',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='image',
            field=sorl.thumbnail.fields.ImageField(max_length=255, width_field=models.IntegerField(default=0), upload_to=musterapp.models._page_upload_to, height_field=models.IntegerField(default=0), default=''),
        ),
    ]
