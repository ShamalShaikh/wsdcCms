# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20161102_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conference.Conf_Paper'),
        ),
    ]
