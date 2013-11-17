
from django.db import models

class Summoner(models.Model):
    summoner_id = models.IntegerField(max_length=200)
    summonerLevel = models.IntegerField(default=0)

