# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-04 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20180104_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='hashtag',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]