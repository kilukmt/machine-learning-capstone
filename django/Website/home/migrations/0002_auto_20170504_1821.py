# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-04 22:21
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(default='c:\\Git\\machine-learning-capstone\\django\\Website\\z_Media\\\\default.jpg', max_length=300, storage=django.core.files.storage.FileSystemStorage(location='c:\\Git\\machine-learning-capstone\\django\\Website\\z_Media\\test_images\\'), upload_to=''),
        ),
    ]
