# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2019-01-25 06:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accomodationpayment',
            name='conf_id',
        ),
        migrations.RemoveField(
            model_name='accomodationpayment',
            name='house_choice',
        ),
        migrations.DeleteModel(
            name='AccomodationPayment',
        ),
    ]
