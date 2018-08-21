# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-20 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0017_auto_20180820_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='comentario',
            field=models.CharField(default='', max_length=280),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='colaboracion',
            name='retroalimentacion',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='participacion',
            name='retroalimentacion',
            field=models.BooleanField(default=False),
        ),
    ]
