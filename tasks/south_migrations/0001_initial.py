# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table('task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tasktype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['institutions.TaskType'])),
            ('week', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['institutions.Week'])),
        ))
        db.send_create_signal(u'tasks', ['Task'])

        # Adding model 'TaskTopic'
        db.create_table('task_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('icon', self.gf('s3direct.fields.S3DirectField')(blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='task_topics', to=orm['tasks.Task'])),
        ))
        db.send_create_signal(u'tasks', ['TaskTopic'])

        # Adding model 'Problem'
        db.create_table('problem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pdf', self.gf('s3direct.fields.S3DirectField')(blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='problems', to=orm['tasks.TaskTopic'])),
        ))
        db.send_create_signal(u'tasks', ['Problem'])

        # Adding model 'Result'
        db.create_table('result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('solver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='results', to=orm['auth.User'])),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(related_name='results', to=orm['tasks.Problem'])),
            ('stars', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal(u'tasks', ['Result'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table('task')

        # Deleting model 'TaskTopic'
        db.delete_table('task_topic')

        # Deleting model 'Problem'
        db.delete_table('problem')

        # Deleting model 'Result'
        db.delete_table('result')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'enrollments.enrollment': {
            'Meta': {'unique_together': "(('student', 'week'),)", 'object_name': 'Enrollment', 'db_table': "'enrollment'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrollments'", 'to': u"orm['auth.User']"}),
            'week': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrollments'", 'to': u"orm['institutions.Week']"})
        },
        u'institutions.precollege': {
            'Meta': {'object_name': 'PreCollege', 'db_table': "'precollege'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'discount1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'discount2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'icon': ('s3direct.fields.S3DirectField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price_per_week': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'weeks_discount1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'weeks_discount2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'})
        },
        u'institutions.season': {
            'Meta': {'object_name': 'Season', 'db_table': "'season'"},
            'begin': ('django.db.models.fields.DateField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'precollege': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seasons'", 'to': u"orm['institutions.PreCollege']"})
        },
        u'institutions.tasktype': {
            'Meta': {'object_name': 'TaskType', 'db_table': "'task_type'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('s3direct.fields.S3DirectField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'precollege': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasktypes'", 'to': u"orm['institutions.PreCollege']"})
        },
        u'institutions.week': {
            'Meta': {'ordering': "('-begin',)", 'object_name': 'Week', 'db_table': "'week'"},
            'begin': ('django.db.models.fields.DateField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'weeks'", 'to': u"orm['institutions.Season']"}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'weeks'", 'symmetrical': 'False', 'through': u"orm['enrollments.Enrollment']", 'to': u"orm['auth.User']"}),
            'tasktypes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'weeks'", 'symmetrical': 'False', 'through': u"orm['tasks.Task']", 'to': u"orm['institutions.TaskType']"})
        },
        u'tasks.problem': {
            'Meta': {'object_name': 'Problem', 'db_table': "'problem'"},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'problems'", 'to': u"orm['tasks.TaskTopic']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pdf': ('s3direct.fields.S3DirectField', [], {'blank': 'True'}),
            'solvers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'problems'", 'symmetrical': 'False', 'through': u"orm['tasks.Result']", 'to': u"orm['auth.User']"})
        },
        u'tasks.result': {
            'Meta': {'object_name': 'Result', 'db_table': "'result'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': u"orm['tasks.Problem']"}),
            'solver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': u"orm['auth.User']"}),
            'stars': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'})
        },
        u'tasks.task': {
            'Meta': {'object_name': 'Task', 'db_table': "'task'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tasktype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['institutions.TaskType']"}),
            'week': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['institutions.Week']"})
        },
        u'tasks.tasktopic': {
            'Meta': {'object_name': 'TaskTopic', 'db_table': "'task_topic'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('s3direct.fields.S3DirectField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'task_topics'", 'to': u"orm['tasks.Task']"})
        }
    }

    complete_apps = ['tasks']