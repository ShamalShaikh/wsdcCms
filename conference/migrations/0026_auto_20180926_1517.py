# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-09-26 09:47
from __future__ import unicode_literals

import conference.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0025_auto_20180908_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conf_paper',
            name='paperfile',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/media/rishu/Local Disk/WSDC/CMS/CMSNITW/protected'), upload_to=conference.models.get_conf_paper_path, validators=[conference.models.validate]),
        ),
        migrations.AlterField(
            model_name='final_paper',
            name='copyright_form',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/media/rishu/Local Disk/WSDC/CMS/CMSNITW/protected'), upload_to=conference.models.get_final_paper_path, validators=[conference.models.validate]),
        ),
        migrations.AlterField(
            model_name='final_paper',
            name='final_file',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/media/rishu/Local Disk/WSDC/CMS/CMSNITW/protected'), upload_to=conference.models.get_final_paper_path, validators=[conference.models.validate]),
        ),
        migrations.AlterField(
            model_name='paper_remark',
            name='remarkFile',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/media/rishu/Local Disk/WSDC/CMS/CMSNITW/protected'), upload_to=conference.models.get_remark_file_path, validators=[conference.models.validate]),
        ),
    ]
