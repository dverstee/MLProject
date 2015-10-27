from django.db import models


class Match(models.Model):
    match_id = models.CharField(max_length=10, primary_key=True)
    team1_is_red = models.BooleanField(default=False)
    nr_premade_team1 = models.IntegerField()
    nr_premade_team2 = models.IntegerField()
    won = models.BooleanField()
    match_type = models.CharField(max_length=40)

    team_1summoner1_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner1')
    team_1summoner2_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner2')
    team_1summoner3_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner3')
    team_1summoner4_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner4')
    team_1summoner5_id = models.ForeignKey('ChampionPlayed', related_name='team_1summoner5')

    team_2summoner1_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner1')
    team_2summoner2_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner2')
    team_2summoner3_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner3')
    team_2summoner4_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner4')
    team_2summoner5_id = models.ForeignKey('ChampionPlayed', related_name='team_2summoner5')

    def __unicode__(self):
        return str(self.match_id)
