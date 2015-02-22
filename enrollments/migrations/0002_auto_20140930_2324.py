# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enrollments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdetail',
            name='week',
            field=models.ForeignKey(to='institutions.Week'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ticketdetail',
            unique_together=set([('ticket', 'week')]),
        ),
        migrations.AddField(
            model_name='ticket',
            name='precollege',
            field=models.ForeignKey(related_name=b'tickets', to='institutions.PreCollege'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='season',
            field=models.ForeignKey(related_name=b'tickets', to='institutions.Season'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='student',
            field=models.ForeignKey(related_name=b'tickets', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrollment',
            name='week',
            field=models.ForeignKey(to='institutions.Week'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('student', 'week')]),
        ),
    ]
