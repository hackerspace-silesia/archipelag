# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-10 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_auto_20180104_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='description',
            field=models.CharField(max_length=10000, null=True),
        ),
    ]