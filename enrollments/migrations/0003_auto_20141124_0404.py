# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0002_auto_20140930_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketdetail',
            name='ticket',
            field=models.ForeignKey(related_name=b'ticket_details', to='enrollments.Ticket'),
        ),
    ]
