# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('number', models.PositiveIntegerField()),
                ('pdf', s3direct.fields.S3DirectField(blank=True)),
            ],
            options={
                'db_table': 'problem',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('stars', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('problem', models.ForeignKey(related_name=b'results', to='tasks.Problem')),
                ('solver', models.ForeignKey(related_name=b'results', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'result',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('tasktype', models.ForeignKey(related_name=b'tasks', to='institutions.TaskType')),
                ('week', models.ForeignKey(related_name=b'tasks', to='institutions.Week')),
            ],
            options={
                'db_table': 'task',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('icon', s3direct.fields.S3DirectField(blank=True)),
                ('task', models.ForeignKey(related_name=b'task_topics', to='tasks.Task')),
            ],
            options={
                'db_table': 'task_topic',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='problem',
            name='course',
            field=models.ForeignKey(related_name=b'problems', to='tasks.TaskTopic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='problem',
            name='solvers',
            field=models.ManyToManyField(related_name=b'problems', through='tasks.Result', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
