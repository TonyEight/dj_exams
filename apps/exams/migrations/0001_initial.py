# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 18:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=700, verbose_name='label')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=700, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='ExamContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scale', models.PositiveIntegerField(default=1, verbose_name='scale')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=700, verbose_name='label')),
            ],
        ),
        migrations.AddField(
            model_name='examcontext',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Question', verbose_name='question'),
        ),
        migrations.AddField(
            model_name='exam',
            name='questions',
            field=models.ManyToManyField(through='exams.ExamContext', to='exams.Question', verbose_name='questions'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='possible_answers', to='exams.Question', verbose_name='question'),
        ),
    ]