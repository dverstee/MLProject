from django.db import models


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

