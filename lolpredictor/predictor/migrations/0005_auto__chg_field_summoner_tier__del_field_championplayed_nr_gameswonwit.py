# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Summoner.tier'
        db.alter_column(u'predictor_summoner', 'tier', self.gf('django.db.models.fields.SmallIntegerField')())
        # Deleting field 'ChampionPlayed.nr_gameswonwithchamp'
        db.delete_column(u'predictor_championplayed', 'nr_gameswonwithchamp')

        # Deleting field 'ChampionPlayed.champid'
        db.delete_column(u'predictor_championplayed', 'champid_id')

        # Adding field 'ChampionPlayed.average_deaths'
        db.add_column(u'predictor_championplayed', 'average_deaths',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ChampionPlayed.average_assists'
        db.add_column(u'predictor_championplayed', 'average_assists',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ChampionPlayed.champion'
        db.add_column(u'predictor_championplayed', 'champion',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=17, to=orm['predictor.Champion']),
                      keep_default=False)

        # Adding field 'ChampionPlayed.average_kills'
        db.add_column(u'predictor_championplayed', 'average_kills',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Summoner.tier'
        db.alter_column(u'predictor_summoner', 'tier', self.gf('django.db.models.fields.CharField')(max_length=40))
        # Adding field 'ChampionPlayed.nr_gameswonwithchamp'
        db.add_column(u'predictor_championplayed', 'nr_gameswonwithchamp',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ChampionPlayed.champid'
        db.add_column(u'predictor_championplayed', 'champid',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['predictor.Champion']),
                      keep_default=False)

        # Deleting field 'ChampionPlayed.average_deaths'
        db.delete_column(u'predictor_championplayed', 'average_deaths')

        # Deleting field 'ChampionPlayed.average_assists'
        db.delete_column(u'predictor_championplayed', 'average_assists')

        # Deleting field 'ChampionPlayed.champion'
        db.delete_column(u'predictor_championplayed', 'champion_id')

        # Deleting field 'ChampionPlayed.average_kills'
        db.delete_column(u'predictor_championplayed', 'average_kills')


    models = {
        u'predictor.champion': {
            'Meta': {'object_name': 'Champion'},
            'attack': ('django.db.models.fields.SmallIntegerField', [], {}),
            'defense': ('django.db.models.fields.SmallIntegerField', [], {}),
            'difficulty': ('django.db.models.fields.SmallIntegerField', [], {}),
            'key': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'magic': ('django.db.models.fields.SmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'predictor.championplayed': {
            'Meta': {'object_name': 'ChampionPlayed'},
            'average_assists': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'average_deaths': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'average_kills': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'champion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['predictor.Champion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr_gameswithchamp': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
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
            'leaguepoints': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {'default': '5'}),
            'recentwinpercentage': ('django.db.models.fields.FloatField', [], {}),
            'tier': ('django.db.models.fields.SmallIntegerField', [], {'default': '5'})
        }
    }

    complete_apps = ['predictor']