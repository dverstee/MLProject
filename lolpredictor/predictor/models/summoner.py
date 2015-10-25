from django.db import models


class Summoner(models.Model):
    summoner_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    region = models.CharField(max_length=20, primary_key=True)
    tier = models.IntegerField()
    rank = models.IntegerField()
    hotstreak = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.name)

    def getDivision(self):
        tiers = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
        divisions = ['I', 'II', 'III', 'IV', 'V']
        return tiers[self.tier - 1] + ' ' + divisions[self.rank - 1]

