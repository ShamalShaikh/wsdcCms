# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-09-11 10:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_auth', '0022_auto_20180911_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='is_aproved',
            new_name='is_aprooved',
        ),
    ]