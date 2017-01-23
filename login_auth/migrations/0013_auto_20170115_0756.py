# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-15 07:56
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import login_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('login_auth', '0012_auto_20170114_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pic_of_dd',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/Users/acemaster/Documents/WSDC/ConferenceManagement/protected'), upload_to=login_auth.models.get_dd_path),
        ),
        migrations.AlterField(
            model_name='payment',
            name='pic_of_id',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/Users/acemaster/Documents/WSDC/ConferenceManagement/protected'), upload_to=login_auth.models.get_dd_path),
        ),
        migrations.AlterField(
            model_name='rejected_payment',
            name='pic_of_dd',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/Users/acemaster/Documents/WSDC/ConferenceManagement/protected'), upload_to=login_auth.models.get_dd_path),
        ),
    ]
