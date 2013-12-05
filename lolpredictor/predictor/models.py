
from django.db import models

class Champion(models.Model):
    name                    = models.CharField(max_length=40)
    key                     = models.SmallIntegerField(primary_key=True)
    difficulty              = models.SmallIntegerField()
    magic                   = models.SmallIntegerField()
    attack                  = models.SmallIntegerField()
    defense                 = models.SmallIntegerField()
    can_jungle              = models.BooleanField(default=False)
    can_mid                 = models.BooleanField(default=False)
    can_top                 = models.BooleanField(default=False)
    can_adc                 = models.BooleanField(default=False)
    can_support             = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class ChampionPlayed(models.Model): 
    champion                = models.ForeignKey('Champion')
    summoner                = models.ForeignKey('Summoner')

    nr_gameswithchamp       = models.SmallIntegerField()
    average_kills           = models.SmallIntegerField()
    average_deaths          = models.SmallIntegerField()
    average_assists         = models.SmallIntegerField()
    average_gold            = models.SmallIntegerField()
    champions_updated_at    = models.DateTimeField(auto_now=True)
 
    class Meta:
        unique_together = (("champion", "summoner"),)

    def __unicode__(self):
        return str(self.champion) +" " +str(self.summoner)

class Summoner(models.Model):
    name                        = models.CharField(max_length=20)
    summoner_id                 = models.CharField(max_length=10)
    account_id                  = models.CharField(max_length=10, primary_key=True)
    tier                        = models.SmallIntegerField()
    rank                        = models.SmallIntegerField()
    hotstreak                   = models.BooleanField ()
    updated_at                  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.name)

    def getDivision(self):
        tiers = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
        divisions = ['I', 'II', 'III', 'IV', 'V']
        return tiers[self.tier-1] + ' ' + divisions[self.rank-1]

class Match(models.Model):
    match_id            = models.CharField(max_length=10, primary_key=True)
    team1_is_red        = models.BooleanField()
    nr_premade_team1    = models.SmallIntegerField()
    nr_premade_team2    = models.SmallIntegerField()
    won                 = models.BooleanField()
    match_type          = models.CharField(max_length=40)

    team_1summoner1_id = models.ForeignKey('ChampionPlayed' , related_name='team_1summoner1')
    team_1summoner2_id = models.ForeignKey('ChampionPlayed' , related_name='team_1summoner2')
    team_1summoner3_id = models.ForeignKey('ChampionPlayed' , related_name='team_1summoner3')
    team_1summoner4_id = models.ForeignKey('ChampionPlayed' , related_name='team_1summoner4')
    team_1summoner5_id = models.ForeignKey('ChampionPlayed' , related_name='team_1summoner5')

    team_2summoner1_id = models.ForeignKey('ChampionPlayed' , related_name='team_2summoner1')
    team_2summoner2_id = models.ForeignKey('ChampionPlayed' , related_name='team_2summoner2')
    team_2summoner3_id = models.ForeignKey('ChampionPlayed' , related_name='team_2summoner3')
    team_2summoner4_id = models.ForeignKey('ChampionPlayed' , related_name='team_2summoner4')
    team_2summoner5_id = models.ForeignKey('ChampionPlayed' , related_name='team_2summoner5')
    def __unicode__(self):
         return str(self.match_id)

class Matchup(models.Model):
    champion_1 = models.ForeignKey('Champion' , related_name='champion_1')
    champion_2 = models.ForeignKey('Champion' , related_name='champion_2')
    win_rate   = models.FloatField()
    