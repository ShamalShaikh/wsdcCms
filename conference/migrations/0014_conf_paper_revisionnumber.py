# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-30 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0013_conf_paper_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='conf_paper',
            name='revisionNumber',
            field=models.IntegerField(default=1),
        ),
    ]
