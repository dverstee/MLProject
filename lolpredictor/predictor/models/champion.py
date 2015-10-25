from django.db import models


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