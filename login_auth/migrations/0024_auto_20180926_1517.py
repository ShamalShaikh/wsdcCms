# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-09-26 09:47
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import login_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('login_auth', '0023_auto_20180911_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pic_of_dd',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/media/rishu/Local Disk/WSDC/CMS/CMSNITW/protected'), upload_to=login_auth.models.get_dd_path),
        ),
        migrations.AlterField(
            model_name='payment',
            name='pic_of_id',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/media/rishu/Local Disk/WSDC/CMS/CMSNITW/protected'), upload_to=login_auth.models.get_dd_path),
        ),
        migrations.AlterField(
            model_name='rejected_payment',
            name='pic_of_dd',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/media/rishu/Local Disk/WSDC/CMS/CMSNITW/protected'), upload_to=login_auth.models.get_dd_path),
        ),
    ]
