from django.shortcuts import render
from api import *
from util import *
import globals

def crawlstats(request):
    stats = {}
    stats['nrOfSummoners'] = Summoner.object.all().count()
    stats['nrOfBronze'] = Summoner.object.filter(tier=1).count()
    stats['nrOfSilver'] = Summoner.object.filter(tier=2).count()
    stats['nrOfGold'] = Summoner.object.filter(tier=3).count()
    stats['nrOfPlatinum'] = Summoner.object.filter(tier=4).count()
    stats['nrOfDiamond'] = Summoner.object.filter(tier=5).count()
    return render(request, 'predictor/crawlstats.html', stats)