# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0019_auto_20150626_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='vector_count',
            field=models.IntegerField(editable=False, default=0),
        ),
    ]
