# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-10 10:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20180215_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created on'),
        ),
    ]