from django.shortcuts import render
from django.db.models import Count
from api import *
from util import *
import globals

def crawlstats(request):
    stats = {}
    stats['nrOfSummoners'] = Summoner.objects.count()
    stats['nrOfBronze'] = Summoner.objects.filter(tier=1).count()
    stats['nrOfSilver'] = Summoner.objects.filter(tier=2).count()
    stats['nrOfGold'] = Summoner.objects.filter(tier=3).count()
    stats['nrOfPlatinum'] = Summoner.objects.filter(tier=4).count()
    stats['nrOfDiamond'] = Summoner.objects.filter(tier=5).count()
    stats['nrOfMatches'] = Match.objects.count()
    stats['nrOfChampionPlayed'] = ChampionPlayed.objects.count()

    stats['summoners'] = Summoner.objects.order_by('name')
    return render(request, 'predictor/crawlstats.html', stats)