# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-27 14:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('conferenceName', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('U', 'Upcoming'), ('P', 'Previous')], max_length=1)),
                ('alias', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('pageName', models.CharField(max_length=20)),
                ('content', models.CharField(max_length=1000)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conferences.Conference')),
            ],
        ),
        migrations.CreateModel(
            name='Papers',
            fields=[
                ('paperid', models.AutoField(primary_key=True, serialize=False)),
                ('pname', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('submissionDate', models.DateField()),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('uname', models.CharField(max_length=20)),
                ('emailId', models.CharField(max_length=35)),
                ('cellNo', models.IntegerField()),
                ('permissions', models.IntegerField()),
                ('password', models.CharField(max_length=16)),
            ],
        ),
        migrations.AddField(
            model_name='conference',
            name='mid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conferences.Users'),
        ),
    ]
