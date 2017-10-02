# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-01 07:39
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import login_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('login_auth', '0015_auto_20170930_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pic_of_dd',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/var/www/html/ConferenceManagement/protected'), upload_to=login_auth.models.get_dd_path),
        ),
        migrations.AlterField(
            model_name='payment',
            name='pic_of_id',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/var/www/html/ConferenceManagement/protected'), upload_to=login_auth.models.get_dd_path),
        ),
        migrations.AlterField(
            model_name='rejected_payment',
            name='pic_of_dd',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/var/www/html/ConferenceManagement/protected'), upload_to=login_auth.models.get_dd_path),
        ),
    ]
