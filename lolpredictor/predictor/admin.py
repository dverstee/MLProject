

# Register your models here.
from django.contrib import admin
from models import *

class ChampionAdmin(admin.ModelAdmin):
    fields = ('key', 'name', 'tags')
    list_display = ('key', 'name', 'tags')
admin.site.register(Champion, ChampionAdmin)

class ChampionPlayedAdmin(admin.ModelAdmin):
    list_display = ('summoner', 'champion', 'nr_gameswithchamp', 'average_kills', 'average_deaths')
admin.site.register(ChampionPlayed, ChampionPlayedAdmin)

admin.site.register(Summoner)
admin.site.register(match)