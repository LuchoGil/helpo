# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-01 04:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_merge_20180828_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceID',
            fields=[
                ('player_id', models.TextField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
    ]