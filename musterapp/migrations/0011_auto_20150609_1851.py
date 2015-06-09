# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musterapp', '0010_pattern'),
    ]

    operations = [
        migrations.CreateModel(
            name='VolumeCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('category', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=8)),
            ],
        ),
        migrations.RemoveField(
            model_name='volume',
            name='object_category',
        ),
        migrations.RemoveField(
            model_name='volume',
            name='object_name',
        ),
        migrations.AddField(
            model_name='volume',
            name='category',
            field=models.ForeignKey(to='musterapp.VolumeCategory', related_name='volumes', default=''),
            preserve_default=False,
        ),
    ]
