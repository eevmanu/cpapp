# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enrollments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreCollege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=200)),
                ('icon', s3direct.fields.S3DirectField(blank=True)),
                ('weeks_discount1', models.PositiveSmallIntegerField(null=True)),
                ('discount1', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('weeks_discount2', models.PositiveSmallIntegerField(null=True)),
                ('discount2', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('price_per_week', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
            ],
            options={
                'db_table': 'precollege',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=200)),
                ('begin', models.DateField()),
                ('end', models.DateField()),
            ],
            options={
                'db_table': 'season',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=200)),
                ('icon', s3direct.fields.S3DirectField(blank=True)),
            ],
            options={
                'db_table': 'task_type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('begin', models.DateField()),
                ('end', models.DateField()),
                ('season', models.ForeignKey(related_name=b'weeks', to='institutions.Season')),
                ('students', models.ManyToManyField(related_name=b'weeks', through='enrollments.Enrollment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-begin',),
                'db_table': 'week',
            },
            bases=(models.Model,),
        ),
    ]
