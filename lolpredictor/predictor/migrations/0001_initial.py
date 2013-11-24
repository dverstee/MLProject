# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChampionPlayed'
        db.create_table(u'predictor_championplayed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nr_gameswithchamp', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('nr_gameswonwithchamp', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('champid', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'predictor', ['ChampionPlayed'])

        # Adding model 'Summoner'
        db.create_table(u'predictor_summoner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('champion_played', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed'])),
            ('leaguepoints', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('tier', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('rank', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('recentwinpercentage', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'predictor', ['Summoner'])

        # Adding model 'match'
        db.create_table(u'predictor_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team1_is_red', self.gf('django.db.models.fields.BooleanField')()),
            ('nr_premade_team1', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('nr_premade_team2', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('won', self.gf('django.db.models.fields.BooleanField')()),
            ('match_type', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('team_1summoner1_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_1summoner1', to=orm['predictor.Summoner'])),
            ('team_1summoner2_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_1summoner2', to=orm['predictor.Summoner'])),
            ('team_1summoner3_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_1summoner3', to=orm['predictor.Summoner'])),
            ('team_1summoner4_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_1summoner4', to=orm['predictor.Summoner'])),
            ('team_1summoner5_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_1summoner5', to=orm['predictor.Summoner'])),
            ('team_2summoner1_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_2summoner1', to=orm['predictor.Summoner'])),
            ('team_2summoner2_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_2summoner2', to=orm['predictor.Summoner'])),
            ('team_2summoner3_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_2summoner3', to=orm['predictor.Summoner'])),
            ('team_2summoner4_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_2summoner4', to=orm['predictor.Summoner'])),
            ('team_2summoner5_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_2summoner5', to=orm['predictor.Summoner'])),
        ))
        db.send_create_signal(u'predictor', ['match'])


    def backwards(self, orm):
        # Deleting model 'ChampionPlayed'
        db.delete_table(u'predictor_championplayed')

        # Deleting model 'Summoner'
        db.delete_table(u'predictor_summoner')

        # Deleting model 'match'
        db.delete_table(u'predictor_match')


    models = {
        u'predictor.championplayed': {
            'Meta': {'object_name': 'ChampionPlayed'},
            'champid': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr_gameswithchamp': ('django.db.models.fields.SmallIntegerField', [], {}),
            'nr_gameswonwithchamp': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'predictor.match': {
            'Meta': {'object_name': 'match'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match_type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'nr_premade_team1': ('django.db.models.fields.SmallIntegerField', [], {}),
            'nr_premade_team2': ('django.db.models.fields.SmallIntegerField', [], {}),
            'team1_is_red': ('django.db.models.fields.BooleanField', [], {}),
            'team_1summoner1_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner1'", 'to': u"orm['predictor.Summoner']"}),
            'team_1summoner2_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner2'", 'to': u"orm['predictor.Summoner']"}),
            'team_1summoner3_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner3'", 'to': u"orm['predictor.Summoner']"}),
            'team_1summoner4_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner4'", 'to': u"orm['predictor.Summoner']"}),
            'team_1summoner5_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner5'", 'to': u"orm['predictor.Summoner']"}),
            'team_2summoner1_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner1'", 'to': u"orm['predictor.Summoner']"}),
            'team_2summoner2_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner2'", 'to': u"orm['predictor.Summoner']"}),
            'team_2summoner3_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner3'", 'to': u"orm['predictor.Summoner']"}),
            'team_2summoner4_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner4'", 'to': u"orm['predictor.Summoner']"}),
            'team_2summoner5_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner5'", 'to': u"orm['predictor.Summoner']"}),
            'won': ('django.db.models.fields.BooleanField', [], {})
        },
        u'predictor.summoner': {
            'Meta': {'object_name': 'Summoner'},
            'champion_played': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['predictor.ChampionPlayed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leaguepoints': ('django.db.models.fields.SmallIntegerField', [], {}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'recentwinpercentage': ('django.db.models.fields.FloatField', [], {}),
            'tier': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['predictor']