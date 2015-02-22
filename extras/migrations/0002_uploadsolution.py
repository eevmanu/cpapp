# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadSolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('solution', models.FileField(upload_to=b'upload')),
            ],
            options={
                'db_table': 'upload_solution',
                'verbose_name': 'Carga masiva',
                'verbose_name_plural': 'Carga masiva de soluciones',
            },
            bases=(models.Model,),
        ),
    ]
