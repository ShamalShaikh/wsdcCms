# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-28 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_auto_20180328_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewer',
            name='papers',
            field=models.ManyToManyField(blank=True, to='conference.Conf_Paper'),
        ),
    ]
