from django.db import models
from lolpredictor.predictor.enums import Region

class Champion(models.Model):
    name = models.CharField(max_length=40)
    key = models.IntegerField(primary_key=True)
    difficulty = models.IntegerField()
    magic = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    can_jungle = models.BooleanField(default=False)
    can_mid = models.BooleanField(default=False)
    can_top = models.BooleanField(default=False)
    can_adc = models.BooleanField(default=False)
    can_support = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class ChampionPlayed(models.Model):
    champion = models.ForeignKey('Champion')
    summoner = models.ForeignKey('Summoner')

    nr_gameswithchamp = models.IntegerField()
    average_kills = models.FloatField()
    average_deaths = models.FloatField()
    average_assists = models.FloatField()
    average_gold = models.FloatField()
    champions_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("champion", "summoner"),)

    def __unicode__(self):
        return str(self.champion) + " " + str(self.summoner)


class Summoner(models.Model):
    summoner_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    region = models.CharField(max_length=20, primary_key=True)
    tier = models.IntegerField()
    rank = models.IntegerField()
    hotstreak = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.name)


    def getDivision(self):
        tiers = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
        divisions = ['I', 'II', 'III', 'IV', 'V']
        return tiers[self.tier - 1] + ' ' + divisions[self.rank - 1]


class Match(models.Model):
    match_id = models.CharField(max_length=10, primary_key=True)
    team1_is_red = models.BooleanField()
    nr_premade_team1 = models.IntegerField()
    nr_premade_team2 = models.IntegerField()
    won = models.BooleanField()
    match_type = models.CharField(max_length=40)

    team_1summoner1_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner1')
    team_1summoner2_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner2')
    team_1summoner3_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner3')
    team_1summoner4_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner4')
    team_1summoner5_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner5')

    team_2summoner1_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner1')
    team_2summoner2_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner2')
    team_2summoner3_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner3')
    team_2summoner4_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner4')
    team_2summoner5_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner5')

    def __unicode__(self):
        return str(self.match_id)


class Matchup(models.Model):
    champion_1 = models.ForeignKey('Champion', related_name='champion_1')
    champion_2 = models.ForeignKey('Champion', related_name='champion_2')
    win_rate = models.FloatField()


class Synergy(models.Model):
    champion_1 = models.ForeignKey('Champion', related_name='champion_a')
    champion_2 = models.ForeignKey('Champion', related_name='champion_b')
    win_rate = models.FloatField()


class PreProcessedMatch(models.Model):
    match_id = models.CharField(max_length=10, primary_key=True)
    team1_is_red = models.BooleanField()
    nr_premade_team1 = models.IntegerField()
    nr_premade_team2 = models.IntegerField()
    won = models.BooleanField()
    match_type = models.CharField(max_length=40)

    team_1_top_score = models.FloatField(default=0)
    team_1_mid_score = models.FloatField(default=0)
    team_1_adc_score = models.FloatField(default=0)
    team_1_supp_score = models.FloatField(default=0)
    team_1_jungle_score = models.FloatField(default=0)

    team_2_top_score = models.FloatField(default=0)
    team_2_mid_score = models.FloatField(default=0)
    team_2_adc_score = models.FloatField(default=0)
    team_2_supp_score = models.FloatField(default=0)
    team_2_jungle_score = models.FloatField(default=0)
