
from django.db import models

class RankedMatch(models.Model):
    team_1_summoner1_id= models.IntegerField(max_length=200)
    team_1_summoner2_id = models.IntegerField(max_length=200)
    team_1_summoner3_id = models.IntegerField(max_length=200)
    team_1_summoner4_id = models.IntegerField(max_length=200)
    team_1_summoner5_id = models.IntegerField(max_length=200)

    team_2_summoner1_id = models.IntegerField(max_length=200)
    team_2_summoner2_id = models.IntegerField(max_length=200)
    team_2_summoner3_id = models.IntegerField(max_length=200)
    team_2_summoner4_id = models.IntegerField(max_length=200)
    team_2_summoner5_id = models.IntegerField(max_length=200)

    team_1_summoner1_champid = models.IntegerField(max_length=200)
    team_1_summoner2_champid = models.IntegerField(max_length=200)
    team_1_summoner3_champid = models.IntegerField(max_length=200)
    team_1_summoner4_champid = models.IntegerField(max_length=200)
    team_1_summoner5_champid = models.IntegerField(max_length=200)

    team_2_summoner1_champid = models.IntegerField(max_length=200)
    team_2_summoner2_champid = models.IntegerField(max_length=200)
    team_2_summoner3_champid = models.IntegerField(max_length=200)
    team_2_summoner4_champid = models.IntegerField(max_length=200)
    team_2_summoner5_champid = models.IntegerField(max_length=200)

class Summoner(models.Model):
    name = models.CharField(max_length=200)