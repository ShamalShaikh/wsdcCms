# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-28 01:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0011_auto_20160828_0142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
