# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Champion'
        db.create_table(u'predictor_champion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('key', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('difficulty', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('magic', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('attack', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('defense', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'predictor', ['Champion'])


    def backwards(self, orm):
        # Deleting model 'Champion'
        db.delete_table(u'predictor_champion')


    models = {
        u'predictor.champion': {
            'Meta': {'object_name': 'Champion'},
            'attack': ('django.db.models.fields.SmallIntegerField', [], {}),
            'defense': ('django.db.models.fields.SmallIntegerField', [], {}),
            'difficulty': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.SmallIntegerField', [], {}),
            'magic': ('django.db.models.fields.SmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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