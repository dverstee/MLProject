# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('name', models.CharField(max_length=40)),
                ('key', models.IntegerField(serialize=False, primary_key=True)),
                ('difficulty', models.IntegerField()),
                ('magic', models.IntegerField()),
                ('attack', models.IntegerField()),
                ('defense', models.IntegerField()),
                ('can_jungle', models.BooleanField(default=False)),
                ('can_mid', models.BooleanField(default=False)),
                ('can_top', models.BooleanField(default=False)),
                ('can_adc', models.BooleanField(default=False)),
                ('can_support', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ChampionPlayed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nr_gameswithchamp', models.IntegerField()),
                ('average_kills', models.FloatField()),
                ('average_deaths', models.FloatField()),
                ('average_assists', models.FloatField()),
                ('average_gold', models.FloatField()),
                ('champions_updated_at', models.DateTimeField(auto_now=True)),
                ('champion', models.ForeignKey(to='predictor.Champion')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('match_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('team1_is_red', models.BooleanField()),
                ('nr_premade_team1', models.IntegerField()),
                ('nr_premade_team2', models.IntegerField()),
                ('won', models.BooleanField()),
                ('match_type', models.CharField(max_length=40)),
                ('team_1summoner1_id', models.ForeignKey(related_name='team_1summoner1', to='predictor.ChampionPlayed')),
                ('team_1summoner2_id', models.ForeignKey(related_name='team_1summoner2', to='predictor.ChampionPlayed')),
                ('team_1summoner3_id', models.ForeignKey(related_name='team_1summoner3', to='predictor.ChampionPlayed')),
                ('team_1summoner4_id', models.ForeignKey(related_name='team_1summoner4', to='predictor.ChampionPlayed')),
                ('team_1summoner5_id', models.ForeignKey(related_name='team_1summoner5', to='predictor.ChampionPlayed')),
                ('team_2summoner1_id', models.ForeignKey(related_name='team_2summoner1', to='predictor.ChampionPlayed')),
                ('team_2summoner2_id', models.ForeignKey(related_name='team_2summoner2', to='predictor.ChampionPlayed')),
                ('team_2summoner3_id', models.ForeignKey(related_name='team_2summoner3', to='predictor.ChampionPlayed')),
                ('team_2summoner4_id', models.ForeignKey(related_name='team_2summoner4', to='predictor.ChampionPlayed')),
                ('team_2summoner5_id', models.ForeignKey(related_name='team_2summoner5', to='predictor.ChampionPlayed')),
            ],
        ),
        migrations.CreateModel(
            name='Matchup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('win_rate', models.FloatField()),
                ('champion_1', models.ForeignKey(related_name='champion_1', to='predictor.Champion')),
                ('champion_2', models.ForeignKey(related_name='champion_2', to='predictor.Champion')),
            ],
        ),
        migrations.CreateModel(
            name='PreProcessedMatch',
            fields=[
                ('match_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('team1_is_red', models.BooleanField()),
                ('nr_premade_team1', models.IntegerField()),
                ('nr_premade_team2', models.IntegerField()),
                ('won', models.BooleanField(default=False)),
                ('match_type', models.CharField(max_length=40)),
                ('team_1_top_score', models.FloatField(default=0)),
                ('team_1_mid_score', models.FloatField(default=0)),
                ('team_1_adc_score', models.FloatField(default=0)),
                ('team_1_supp_score', models.FloatField(default=0)),
                ('team_1_jungle_score', models.FloatField(default=0)),
                ('team_2_top_score', models.FloatField(default=0)),
                ('team_2_mid_score', models.FloatField(default=0)),
                ('team_2_adc_score', models.FloatField(default=0)),
                ('team_2_supp_score', models.FloatField(default=0)),
                ('team_2_jungle_score', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('summoner_id', models.IntegerField(primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('region', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('tier', models.IntegerField()),
                ('rank', models.IntegerField()),
                ('hotstreak', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Synergy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('win_rate', models.FloatField()),
                ('champion_1', models.ForeignKey(related_name='champion_a', to='predictor.Champion')),
                ('champion_2', models.ForeignKey(related_name='champion_b', to='predictor.Champion')),
            ],
        ),
        migrations.AddField(
            model_name='championplayed',
            name='summoner',
            field=models.ForeignKey(to='predictor.Summoner'),
        ),
        migrations.AlterUniqueTogether(
            name='championplayed',
            unique_together=set([('champion', 'summoner')]),
        ),
    ]
