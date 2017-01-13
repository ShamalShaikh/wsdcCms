# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-27 09:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0004_auto_20161103_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=200)),
                ('branch_alias', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='conference',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conference.Branch'),
        ),
    ]