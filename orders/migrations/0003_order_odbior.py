# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-13 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20170905_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='odbior',
            field=models.BooleanField(default=True, verbose_name='Odbiór osobisty'),
        ),
    ]