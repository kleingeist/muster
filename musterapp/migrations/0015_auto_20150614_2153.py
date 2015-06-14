# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import musterapp.models
import sorl.thumbnail.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('musterapp', '0014_auto_20150610_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='pattern',
            name='image',
            field=sorl.thumbnail.fields.ImageField(default='', null=True, max_length=255, upload_to=musterapp.models._pattern_upload_to, blank=True, height_field='image_height', width_field='image_width'),
        ),
    ]
