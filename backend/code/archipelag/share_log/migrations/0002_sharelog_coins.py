# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-10 18:21
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_log', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharelog',
            name='coins',
            field=models.DecimalField(decimal_places=1, default=10.0, max_digits=100, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
