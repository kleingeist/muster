# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import musterapp.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('record_id', models.CharField(unique=True, max_length=32)),
                ('number', models.SmallIntegerField(default=-1)),
                ('img_name', models.CharField(max_length=255)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=musterapp.models._page_upload_to, default='')),
                ('object_name', models.CharField(max_length=255)),
                ('object_category', models.CharField(max_length=255)),
                ('general_desc', models.TextField(blank=True)),
                ('physical_desc', models.TextField(blank=True)),
                ('page_width', models.FloatField()),
                ('page_height', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PageColor',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('record_id', models.CharField(unique=True, max_length=32)),
                ('title', models.CharField(max_length=255)),
                ('object_name', models.CharField(max_length=255)),
                ('object_category', models.CharField(max_length=255)),
                ('general_desc', models.TextField(blank=True)),
                ('physical_desc', models.TextField(blank=True)),
                ('page_width', models.FloatField()),
                ('page_height', models.FloatField()),
                ('producer_name', models.CharField(blank=True, max_length=255)),
                ('producer_role', models.CharField(blank=True, max_length=255)),
                ('producer_location', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='colors',
            field=models.ManyToManyField(to='musterapp.PageColor'),
        ),
        migrations.AddField(
            model_name='page',
            name='types',
            field=models.ManyToManyField(to='musterapp.PageType'),
        ),
        migrations.AddField(
            model_name='page',
            name='volume',
            field=models.ForeignKey(related_name='pages', to='musterapp.Volume'),
        ),
    ]
