# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0004_auto_20160605_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='is_published',
            field=models.BooleanField(default=1, verbose_name='is published'),
        ),
    ]
