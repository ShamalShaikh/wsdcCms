# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-02 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0005_auto_20161227_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='conference_alias',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]