# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Summoner.champion_played'
        db.delete_column(u'predictor_summoner', 'champion_played_id')

        # Deleting field 'Summoner.id'
        db.delete_column(u'predictor_summoner', u'id')

        # Deleting field 'Summoner.leaguepoints'
        db.delete_column(u'predictor_summoner', 'leaguepoints')

        # Adding field 'Summoner.name'
        db.add_column(u'predictor_summoner', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Adding field 'Summoner.summoner_id'
        db.add_column(u'predictor_summoner', 'summoner_id',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=10),
                      keep_default=False)

        # Adding field 'Summoner.account_id'
        db.add_column(u'predictor_summoner', 'account_id',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=10, primary_key=True),
                      keep_default=False)

        # Adding field 'Summoner.updated_at'
        db.add_column(u'predictor_summoner', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 11, 25, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'ChampionPlayed.summoner'
        db.add_column(u'predictor_championplayed', 'summoner',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['predictor.Summoner']),
                      keep_default=False)

        # Adding field 'ChampionPlayed.average_gold'
        db.add_column(u'predictor_championplayed', 'average_gold',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'match.match_id'
        db.add_column(u'predictor_match', 'match_id',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=10),
                      keep_default=False)


        # Changing field 'match.team_2summoner4_id'
        db.alter_column(u'predictor_match', 'team_2summoner4_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

        # Changing field 'match.team_1summoner5_id'
        db.alter_column(u'predictor_match', 'team_1summoner5_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

        # Changing field 'match.team_2summoner2_id'
        db.alter_column(u'predictor_match', 'team_2summoner2_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

        # Changing field 'match.team_1summoner1_id'
        db.alter_column(u'predictor_match', 'team_1summoner1_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

        # Changing field 'match.team_2summoner3_id'
        db.alter_column(u'predictor_match', 'team_2summoner3_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

        # Changing field 'match.team_1summoner3_id'
        db.alter_column(u'predictor_match', 'team_1summoner3_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

        # Changing field 'match.team_2summoner5_id'
        db.alter_column(u'predictor_match', 'team_2summoner5_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

        # Changing field 'match.team_1summoner2_id'
        db.alter_column(u'predictor_match', 'team_1summoner2_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

        # Changing field 'match.team_2summoner1_id'
        db.alter_column(u'predictor_match', 'team_2summoner1_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

        # Changing field 'match.team_1summoner4_id'
        db.alter_column(u'predictor_match', 'team_1summoner4_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.ChampionPlayed']))

    def backwards(self, orm):
        # Adding field 'Summoner.champion_played'
        db.add_column(u'predictor_summoner', 'champion_played',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=17, to=orm['predictor.ChampionPlayed']),
                      keep_default=False)

        # Adding field 'Summoner.id'
        db.add_column(u'predictor_summoner', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True),
                      keep_default=False)

        # Adding field 'Summoner.leaguepoints'
        db.add_column(u'predictor_summoner', 'leaguepoints',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Summoner.name'
        db.delete_column(u'predictor_summoner', 'name')

        # Deleting field 'Summoner.summoner_id'
        db.delete_column(u'predictor_summoner', 'summoner_id')

        # Deleting field 'Summoner.account_id'
        db.delete_column(u'predictor_summoner', 'account_id')

        # Deleting field 'Summoner.updated_at'
        db.delete_column(u'predictor_summoner', 'updated_at')

        # Deleting field 'ChampionPlayed.summoner'
        db.delete_column(u'predictor_championplayed', 'summoner_id')

        # Deleting field 'ChampionPlayed.average_gold'
        db.delete_column(u'predictor_championplayed', 'average_gold')

        # Deleting field 'match.match_id'
        db.delete_column(u'predictor_match', 'match_id')


        # Changing field 'match.team_2summoner4_id'
        db.alter_column(u'predictor_match', 'team_2summoner4_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

        # Changing field 'match.team_1summoner5_id'
        db.alter_column(u'predictor_match', 'team_1summoner5_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

        # Changing field 'match.team_2summoner2_id'
        db.alter_column(u'predictor_match', 'team_2summoner2_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

        # Changing field 'match.team_1summoner1_id'
        db.alter_column(u'predictor_match', 'team_1summoner1_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

        # Changing field 'match.team_2summoner3_id'
        db.alter_column(u'predictor_match', 'team_2summoner3_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

        # Changing field 'match.team_1summoner3_id'
        db.alter_column(u'predictor_match', 'team_1summoner3_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

        # Changing field 'match.team_2summoner5_id'
        db.alter_column(u'predictor_match', 'team_2summoner5_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

        # Changing field 'match.team_1summoner2_id'
        db.alter_column(u'predictor_match', 'team_1summoner2_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

        # Changing field 'match.team_2summoner1_id'
        db.alter_column(u'predictor_match', 'team_2summoner1_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

        # Changing field 'match.team_1summoner4_id'
        db.alter_column(u'predictor_match', 'team_1summoner4_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['predictor.Summoner']))

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
            'average_assists': ('django.db.models.fields.SmallIntegerField', [], {}),
            'average_deaths': ('django.db.models.fields.SmallIntegerField', [], {}),
            'average_gold': ('django.db.models.fields.SmallIntegerField', [], {}),
            'average_kills': ('django.db.models.fields.SmallIntegerField', [], {}),
            'champion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['predictor.Champion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr_gameswithchamp': ('django.db.models.fields.SmallIntegerField', [], {}),
            'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['predictor.Summoner']"})
        },
        u'predictor.match': {
            'Meta': {'object_name': 'match'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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
        u'predictor.summoner': {
            'Meta': {'object_name': 'Summoner'},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'recentwinpercentage': ('django.db.models.fields.FloatField', [], {}),
            'summoner_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tier': ('django.db.models.fields.SmallIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['predictor']