from django.db import models


class Matchup(models.Model):
    champion_1 = models.ForeignKey('Champion', related_name='champion_1')
    champion_2 = models.ForeignKey('Champion', related_name='champion_2')
    win_rate = models.FloatField()

