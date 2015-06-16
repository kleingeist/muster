# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('musterapp', '0015_auto_20150614_2153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('file', models.FileField(default=None, max_length=255, blank=True, upload_to='vectors/%Y/%m', null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('pattern', models.ForeignKey(to='musterapp.Pattern', related_name='vectors')),
            ],
        ),
    ]
