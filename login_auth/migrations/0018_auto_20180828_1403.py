# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-28 08:33
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import login_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('login_auth', '0017_auto_20180828_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pic_of_dd',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/cms/ConferenceManagement/protected'), upload_to=login_auth.models.get_dd_path),
        ),
        migrations.AlterField(
            model_name='payment',
            name='pic_of_id',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/cms/ConferenceManagement/protected'), upload_to=login_auth.models.get_dd_path),
        ),
        migrations.AlterField(
            model_name='rejected_payment',
            name='pic_of_dd',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/cms/ConferenceManagement/protected'), upload_to=login_auth.models.get_dd_path),
        ),
    ]
