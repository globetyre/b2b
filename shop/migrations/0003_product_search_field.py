# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-06 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20170905_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='search_field',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Szukajka'),
        ),
    ]
