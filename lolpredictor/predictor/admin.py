
# Register your models here.
from django.contrib import admin
from models import *

class ChampionAdmin(admin.ModelAdmin):
    fields = \
    ('key', 'name', 'can_jungle', 'can_mid', 'can_top', 'can_adc', 'can_support', 'difficulty', 'magic', 'attack',
    'defense')
    list_display = ('key', 'name')


admin.site.register(Champion, ChampionAdmin)


class ChampionPlayedAdmin(admin.ModelAdmin):
    list_display = ('summoner', 'champion', 'nr_gameswithchamp', 'average_kills', 'average_deaths')


admin.site.register(ChampionPlayed, ChampionPlayedAdmin)


class MatchAdmin(admin.ModelAdmin):
    raw_id_fields = ('team_1summoner1_id',
                     'team_1summoner1_id',
                     'team_1summoner2_id',
                     'team_1summoner3_id',
                     'team_1summoner4_id',
                     'team_1summoner5_id',
                     'team_2summoner1_id',
                     'team_2summoner2_id',
                     'team_2summoner3_id',
                     'team_2summoner4_id',
                     'team_2summoner5_id')
    list_display = ('match_id',)


admin.site.register(Summoner)
admin.site.register(Match, MatchAdmin)


class MatchupAdmin(admin.ModelAdmin):
    list_display = ("champion_1", "champion_2", "win_rate")


admin.site.register(Matchup, MatchupAdmin)


class SynergyAdmin(admin.ModelAdmin):
    list_display = ("champion_1", "champion_2", "win_rate")


admin.site.register(Synergy, SynergyAdmin)

admin.site.register(ApiKey)