# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-23 02:43
from __future__ import unicode_literals

import conference.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0011_auto_20170115_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conf_paper',
            name='paperfile',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/priyam/CMS-WSDC/ececonf/ConferenceManagement/protected'), upload_to=conference.models.get_conf_paper_path, validators=[conference.models.validate]),
        ),
        migrations.AlterField(
            model_name='final_paper',
            name='copyright_form',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/priyam/CMS-WSDC/ececonf/ConferenceManagement/protected'), upload_to=conference.models.get_final_paper_path, validators=[conference.models.validate]),
        ),
        migrations.AlterField(
            model_name='final_paper',
            name='final_file',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/priyam/CMS-WSDC/ececonf/ConferenceManagement/protected'), upload_to=conference.models.get_final_paper_path, validators=[conference.models.validate]),
        ),
    ]