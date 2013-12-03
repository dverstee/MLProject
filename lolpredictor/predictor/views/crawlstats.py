from django.shortcuts import render
from api import *
from util import *
import globals

def crawlstats(request):
    stats = {}
    stats['nrOfSummoners'] = Summoner.objects.all().count()
    stats['nrOfBronze'] = Summoner.objects.filter(tier=1).count()
    stats['nrOfSilver'] = Summoner.objects.filter(tier=2).count()
    stats['nrOfGold'] = Summoner.objects.filter(tier=3).count()
    stats['nrOfPlatinum'] = Summoner.objects.filter(tier=4).count()
    stats['nrOfDiamond'] = Summoner.objects.filter(tier=5).count()
    return render(request, 'predictor/crawlstats.html', stats)