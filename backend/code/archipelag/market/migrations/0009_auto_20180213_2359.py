# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-13 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0008_auto_20180213_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_path',
            field=models.ImageField(blank=True, null=True, upload_to='market/images/'),
        ),
    ]