# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        ('institutions', '0001_initial'),
        ('enrollments', '0002_auto_20140930_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='tasktypes',
            field=models.ManyToManyField(related_name=b'weeks', through='tasks.Task', to='institutions.TaskType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='week',
            name='tickets',
            field=models.ManyToManyField(related_name=b'weeks', through='enrollments.TicketDetail', to='enrollments.Ticket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tasktype',
            name='precollege',
            field=models.ForeignKey(related_name=b'tasktypes', to='institutions.PreCollege'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='season',
            name='precollege',
            field=models.ForeignKey(related_name=b'seasons', to='institutions.PreCollege'),
            preserve_default=True,
        ),
    ]
