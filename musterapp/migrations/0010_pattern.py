# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0009_auto_20150530_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('bbox', models.CharField(max_length=79)),
                ('shape', models.TextField(blank=True)),
                ('page', models.ForeignKey(related_name='patterns', to='musterapp.Page')),
            ],
        ),
    ]
