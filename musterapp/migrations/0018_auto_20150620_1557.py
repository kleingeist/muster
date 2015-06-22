# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0017_auto_20150616_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pattern',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', help_text='A comma-separated list of tags.', verbose_name='Tags', blank=True, through='taggit.TaggedItem'),
        ),
    ]
