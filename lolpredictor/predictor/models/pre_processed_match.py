from django.db import models


class PreProcessedMatch(models.Model):
    match_id = models.CharField(max_length=10, primary_key=True)
    team1_is_red = models.BooleanField()
    nr_premade_team1 = models.IntegerField()
    nr_premade_team2 = models.IntegerField()
    won = models.BooleanField()
    match_type = models.CharField(max_length=40)

    team_1_top_score = models.FloatField(default=0)
    team_1_mid_score = models.FloatField(default=0)
    team_1_adc_score = models.FloatField(default=0)
    team_1_supp_score = models.FloatField(default=0)
    team_1_jungle_score = models.FloatField(default=0)

    team_2_top_score = models.FloatField(default=0)
    team_2_mid_score = models.FloatField(default=0)
    team_2_adc_score = models.FloatField(default=0)
    team_2_supp_score = models.FloatField(default=0)
    team_2_jungle_score = models.FloatField(default=0)
