# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-05 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0005_auto_20170505_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='latest_submission',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='latest_submission'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='date_created',
            field=models.DateTimeField(verbose_name='date_created'),
        ),
    ]
