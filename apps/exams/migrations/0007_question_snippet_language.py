# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0006_question_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='snippet_language',
            field=models.CharField(choices=[('python', 'Python'), ('html', 'HTML'), ('css', 'CSS'), ('javascript', 'JavaScript')], max_length=200, null=True, verbose_name='snippet language'),
        ),
    ]
