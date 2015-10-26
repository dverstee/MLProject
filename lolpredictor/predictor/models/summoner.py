from django.db import models


class Summoner(models.Model):
    summoner_id = models.IntegerField(null=False)
    name = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    tier = models.IntegerField()
    rank = models.IntegerField()
    hotstreak = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        unique_together = (("summoner_id", "region"),)

    def getDivision(self):
        tiers = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
        divisions = ['I', 'II', 'III', 'IV', 'V']
        return tiers[self.tier - 1] + ' ' + divisions[self.rank - 1]

