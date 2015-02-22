# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_auto_20140930_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='MsgStudentInSeason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('msg', models.TextField()),
                ('precollege', models.ForeignKey(to='institutions.PreCollege')),
            ],
            options={
                'db_table': 'msg_student_in_season',
                'verbose_name': 'Enviar mensaje',
                'verbose_name_plural': 'Mensajes hacia temporada activa de una cepre',
            },
            bases=(models.Model,),
        ),
    ]
