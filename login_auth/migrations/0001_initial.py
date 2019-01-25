# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2019-01-24 13:38
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import login_auth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('houseName', models.CharField(max_length=255)),
                ('tariff', models.IntegerField()),
                ('house_id', models.IntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'female')], max_length=15)),
                ('seatsAvailable', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AccomodationPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default=None, max_length=255)),
                ('paper_id', models.CharField(blank=True, default=None, max_length=255)),
                ('reference_number', models.CharField(default=None, max_length=255)),
                ('payment_receipt', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/cms/ConferenceManagement/protected/'), upload_to=login_auth.models.get_acc_path)),
                ('is_aprooved', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('review', models.CharField(default='', max_length=500)),
                ('start_date', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('conf_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='conference.Conference')),
                ('house_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_auth.Accomodation')),
            ],
        ),
        migrations.CreateModel(
            name='Alumani',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(blank=True, max_length=255)),
                ('year', models.CharField(blank=True, max_length=255)),
                ('branch', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Delegates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('delegate', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('payment_mode', models.CharField(choices=[('net', 'Net Banking'), ('dd', 'Through DD'), ('neft', 'NEFT')], max_length=20)),
                ('pic_of_dd', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/cms/ConferenceManagement/protected/'), upload_to=login_auth.models.get_dd_path)),
                ('pic_of_id', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/cms/ConferenceManagement/protected/'), upload_to=login_auth.models.get_dd_path)),
                ('refno', models.CharField(default='NA', max_length=20)),
                ('is_aprooved', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('remarks', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(null=True)),
                ('conf_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conference.Conference')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registered_Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conf_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conference.Conference')),
                ('papers', models.ManyToManyField(blank=True, to='conference.Conf_Paper')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rejected_payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic_of_dd', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/home/cms/ConferenceManagement/protected/'), upload_to=login_auth.models.get_dd_path)),
                ('refno', models.CharField(default='NA', max_length=20)),
                ('date', models.DateField()),
                ('remarks', models.CharField(blank=True, max_length=50, null=True)),
                ('conf_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conference.Conference')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SponsorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orgName', models.CharField(max_length=255)),
                ('orgType', models.CharField(max_length=255, null=True)),
                ('md_cco', models.CharField(max_length=255)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255, null=True)),
                ('contact', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=255)),
                ('advertisement', models.FileField(blank=True, null=True, upload_to=login_auth.models.get_adv_path, validators=[login_auth.models.validate])),
                ('conf', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='conference.Conference')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sponsProfile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=20, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('institute', models.CharField(max_length=255, null=True)),
                ('profilepic', models.ImageField(blank=True, null=True, upload_to=login_auth.models.get_user_profile_picture_path)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('department', models.CharField(blank=True, max_length=255, null=True)),
                ('designation', models.CharField(blank=True, max_length=255)),
                ('affiliation', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=1000)),
                ('qualification', models.CharField(blank=True, max_length=255)),
                ('mail_sent_register', models.BooleanField(default=False)),
                ('mail_sent_accept', models.BooleanField(default=False)),
                ('mail_sent_reject', models.BooleanField(default=False)),
                ('alumani', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login_auth.Alumani')),
                ('regConferences', models.ManyToManyField(blank=True, to='login_auth.Registered_Conference')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='delegates',
            name='sponsor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_auth.SponsorProfile'),
        ),
    ]
