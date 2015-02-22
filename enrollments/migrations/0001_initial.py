# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
            ],
            options={
                'db_table': 'enrollment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('number', models.PositiveIntegerField(unique=True)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('active', models.BooleanField(default=True)),
                ('valid_until', models.DateTimeField()),
                ('paid', models.BooleanField(default=False)),
                ('paid_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'ticket',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('ticket', models.ForeignKey(to='enrollments.Ticket')),
            ],
            options={
                'db_table': 'ticket_detail',
            },
            bases=(models.Model,),
        ),
    ]
