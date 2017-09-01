# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-01 12:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nazwa firmy')),
                ('nip', models.CharField(blank=True, max_length=50, null=True, verbose_name='NIP')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Adres')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Kod pocztowy')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Miasto')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Kraj')),
                ('delivery_time', models.CharField(blank=True, max_length=10, null=True, verbose_name='Czas dostawy')),
                ('delivery_price', models.FloatField(blank=True, null=True, verbose_name='Koszt dostawy')),
                ('b2b', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profil',
                'verbose_name_plural': 'Profile',
            },
        ),
    ]
