# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Synergy'
        db.create_table(u'predictor_synergy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('champion_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='champion_a', to=orm['predictor.Champion'])),
            ('champion_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='champion_b', to=orm['predictor.Champion'])),
            ('win_rate', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'predictor', ['Synergy'])


    def backwards(self, orm):
        # Deleting model 'Synergy'
        db.delete_table(u'predictor_synergy')


    models = {
        u'predictor.champion': {
            'Meta': {'object_name': 'Champion'},
            'attack': ('django.db.models.fields.SmallIntegerField', [], {}),
            'can_adc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_jungle': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_mid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_support': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'defense': ('django.db.models.fields.SmallIntegerField', [], {}),
            'difficulty': ('django.db.models.fields.SmallIntegerField', [], {}),
            'key': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'magic': ('django.db.models.fields.SmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'predictor.championplayed': {
            'Meta': {'unique_together': "(('champion', 'summoner'),)", 'object_name': 'ChampionPlayed'},
            'average_assists': ('django.db.models.fields.SmallIntegerField', [], {}),
            'average_deaths': ('django.db.models.fields.SmallIntegerField', [], {}),
            'average_gold': ('django.db.models.fields.SmallIntegerField', [], {}),
            'average_kills': ('django.db.models.fields.SmallIntegerField', [], {}),
            'champion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['predictor.Champion']"}),
            'champions_updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr_gameswithchamp': ('django.db.models.fields.SmallIntegerField', [], {}),
            'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['predictor.Summoner']"})
        },
        u'predictor.match': {
            'Meta': {'object_name': 'Match'},
            'match_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'match_type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'nr_premade_team1': ('django.db.models.fields.SmallIntegerField', [], {}),
            'nr_premade_team2': ('django.db.models.fields.SmallIntegerField', [], {}),
            'team1_is_red': ('django.db.models.fields.BooleanField', [], {}),
            'team_1summoner1_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner1'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'team_1summoner2_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner2'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'team_1summoner3_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner3'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'team_1summoner4_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner4'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'team_1summoner5_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_1summoner5'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'team_2summoner1_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner1'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'team_2summoner2_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner2'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'team_2summoner3_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner3'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'team_2summoner4_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner4'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'team_2summoner5_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_2summoner5'", 'to': u"orm['predictor.ChampionPlayed']"}),
            'won': ('django.db.models.fields.BooleanField', [], {})
        },
        u'predictor.matchup': {
            'Meta': {'object_name': 'Matchup'},
            'champion_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'champion_1'", 'to': u"orm['predictor.Champion']"}),
            'champion_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'champion_2'", 'to': u"orm['predictor.Champion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'win_rate': ('django.db.models.fields.FloatField', [], {})
        },
        u'predictor.summoner': {
            'Meta': {'object_name': 'Summoner'},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'hotstreak': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'summoner_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tier': ('django.db.models.fields.SmallIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'predictor.synergy': {
            'Meta': {'object_name': 'Synergy'},
            'champion_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'champion_a'", 'to': u"orm['predictor.Champion']"}),
            'champion_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'champion_b'", 'to': u"orm['predictor.Champion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'win_rate': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['predictor']