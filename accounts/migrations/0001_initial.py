# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CPProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('first_name', models.CharField(max_length=100, blank=True)),
                ('last_name', models.CharField(max_length=100, blank=True)),
                ('photo', s3direct.fields.S3DirectField(blank=True)),
                ('password_reset_token', models.CharField(default=b'', max_length=400, blank=True)),
                ('device_id', models.TextField(default=b'', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cp_profile',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FBProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('fb_id', models.BigIntegerField(unique=True)),
                ('email', models.EmailField(max_length=100, blank=True)),
                ('token', models.TextField(default=b'', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fb_profile',
            },
            bases=(models.Model,),
        ),
    ]
