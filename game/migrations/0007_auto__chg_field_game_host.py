# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Game.host'
        db.alter_column(u'game_game', 'host_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['game.MemoUser']))

    def backwards(self, orm):

        # Changing field 'Game.host'
        db.alter_column(u'game_game', 'host_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['game.MemoUser']))

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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'game.configuration': {
            'Meta': {'object_name': 'Configuration'},
            'charValue': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intValue': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hosted_games_set'", 'null': 'True', 'to': u"orm['game.MemoUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['game.MemoUser']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'WA'", 'max_length': '2'})
        },
        u'game.memouser': {
            'Meta': {'object_name': 'MemoUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'game.statistic': {
            'Meta': {'object_name': 'Statistic'},
            'charValue': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intValue': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.MemoUser']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['game']