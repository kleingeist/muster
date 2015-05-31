# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0005_auto_20150526_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='image_meta',
        ),
    ]
