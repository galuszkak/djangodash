# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Configuration'
        db.create_table(u'game_configuration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('type', self.gf('django.db.models.fields.TextField')(max_length=3)),
            ('value', self.gf('django.db.models.fields.TextField')(max_length=10)),
        ))
        db.send_create_signal(u'game', ['Configuration'])

        # Adding model 'Game'
        db.create_table(u'game_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.TextField')(default='IN', max_length=2)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=255, null=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hosted_games_set',
                                                                           to=orm['game.MemoUser'])),
        ))
        db.send_create_signal(u'game', ['Game'])

        # Adding M2M table for field players on 'Game'
        m2m_table_name = db.shorten_name(u'game_game_players')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm[u'game.game'], null=False)),
            ('memouser', models.ForeignKey(orm[u'game.memouser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['game_id', 'memouser_id'])

        # Adding model 'Statistic'
        db.create_table(u'game_statistic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('type', self.gf('django.db.models.fields.TextField')(max_length=3)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.MemoUser'], null=True)),
            ('value', self.gf('django.db.models.fields.TextField')(max_length=10)),
        ))
        db.send_create_signal(u'game', ['Statistic'])


    def backwards(self, orm):
        # Deleting model 'Configuration'
        db.delete_table(u'game_configuration')

        # Deleting model 'Game'
        db.delete_table(u'game_game')

        # Removing M2M table for field players on 'Game'
        db.delete_table(db.shorten_name(u'game_game_players'))

        # Deleting model 'Statistic'
        db.delete_table(u'game_statistic')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'game.configuration': {
            'Meta': {'object_name': 'Configuration'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.TextField', [], {'max_length': '3'}),
            'value': ('django.db.models.fields.TextField', [], {'max_length': '10'})
        },
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [],
                     {'related_name': "'hosted_games_set'", 'to': u"orm['game.MemoUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [],
                        {'to': u"orm['game.MemoUser']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.TextField', [], {'default': "'IN'", 'max_length': '2'})
        },
        u'game.memouser': {
            'Meta': {'object_name': 'MemoUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'game.statistic': {
            'Meta': {'object_name': 'Statistic'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.MemoUser']", 'null': 'True'}),
            'type': ('django.db.models.fields.TextField', [], {'max_length': '3'}),
            'value': ('django.db.models.fields.TextField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['game']