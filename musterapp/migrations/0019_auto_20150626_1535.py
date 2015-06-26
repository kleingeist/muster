# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('musterapp', '0018_auto_20150620_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='VectorRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='vector',
            name='rating',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='vectorrating',
            name='vector',
            field=models.ForeignKey(to='musterapp.Vector', related_name='ratings'),
        ),
    ]
