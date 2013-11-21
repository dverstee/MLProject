
from django.db import models


class ChampionPlayed(models.Model): 

    nr_gameswithchamp       = models.SmallIntegerField()
    nr_gameswonwithchamp    = models.SmallIntegerField()
    champid                 = models.SmallIntegerField()

    def __unicode__(self):
        return self.id()


class Summoner(models.Model):


    champion_played             = models.ForeignKey('ChampionPlayed')
    leaguepoints                = models.SmallIntegerField()
    tier                        = models.CharField(max_length=40)
    rank                        = models.SmallIntegerField()
    recentwinpercentage         = models.FloatField ()

    def __unicode__(self):
        return self.id()

class match(models.Model):


    team1_is_red        = models.BooleanField()
    nr_premade_team1    = models.SmallIntegerField()
    nr_premade_team2    = models.SmallIntegerField()
    won                 = models.BooleanField()
    

    team_1summoner1_id = models.ForeignKey('Summoner' , related_name='team_1summoner1')
    team_1summoner2_id = models.ForeignKey('Summoner' , related_name='team_1summoner2')
    team_1summoner3_id = models.ForeignKey('Summoner' , related_name='team_1summoner3')
    team_1summoner4_id = models.ForeignKey('Summoner' , related_name='team_1summoner4')
    team_1summoner5_id = models.ForeignKey('Summoner' , related_name='team_1summoner5')

    team_2summoner1_id = models.ForeignKey('Summoner' , related_name='team_2summoner1')
    team_2summoner2_id = models.ForeignKey('Summoner' , related_name='team_2summoner2')
    team_2summoner3_id = models.ForeignKey('Summoner' , related_name='team_2summoner3')
    team_2summoner4_id = models.ForeignKey('Summoner' , related_name='team_2summoner4')
    team_2summoner5_id = models.ForeignKey('Summoner' , related_name='team_2summoner5')

    def __unicode__(self):
         return self.id()


