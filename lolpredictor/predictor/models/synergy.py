from django.db import models


class Synergy(models.Model):
    champion_1 = models.ForeignKey('Champion', related_name='champion_a')
    champion_2 = models.ForeignKey('Champion', related_name='champion_b')
    win_rate = models.FloatField()

