# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0003_conf_paper_is_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='conf_paper',
            name='under_review',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='conference',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Manager'),
        ),
    ]
