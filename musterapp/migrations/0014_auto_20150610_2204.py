# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import musterapp.fields


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0013_auto_20150610_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pattern',
            name='bbox',
            field=musterapp.fields.BBoxField(),
        ),
    ]
