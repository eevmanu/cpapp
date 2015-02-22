# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_auto_20140930_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='publication',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 26, 0, 12, 39, 46553)),
            preserve_default=False,
        ),
    ]
