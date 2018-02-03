# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-30 13:01
from __future__ import unicode_literals

import conference.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0014_conf_paper_revisionnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper_remark',
            name='remarkFile',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/priyam/CMS-WSDC/ececonf/ConferenceManagement/protected'), upload_to=conference.models.get_remark_file_path, validators=[conference.models.validate]),
        ),
    ]