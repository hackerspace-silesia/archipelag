# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-19 22:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('market', '0009_auto_20180213_2359'),
        ('ngo', '0004_auto_20180211_1942'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Market')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ngo.NgoUser')),
            ],
        ),
    ]
