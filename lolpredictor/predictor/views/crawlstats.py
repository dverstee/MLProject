from django.shortcuts import render
from lolpredictor.predictor.enums import Tier
from lolpredictor.predictor.models import Summoner, Match, ChampionPlayed


def crawlstats(request):
    stats = {}
    stats['nrOfSummoners'] = Summoner.objects.count()
    stats['nrOfBronze'] = Summoner.objects.filter(tier=Tier.BRONZE.value).count()
    stats['nrOfSilver'] = Summoner.objects.filter(tier=Tier.SILVER.value).count()
    stats['nrOfGold'] = Summoner.objects.filter(tier=Tier.GOLD.value).count()
    stats['nrOfPlatinum'] = Summoner.objects.filter(tier=Tier.PLATINUM.value).count()
    stats['nrOfDiamond'] = Summoner.objects.filter(tier=Tier.DIAMOND.value).count()
    stats['nrOfMatches'] = Match.objects.count()
    stats['nrOfChampionPlayed'] = ChampionPlayed.objects.count()
    return render(request, 'predictor/crawlstats.html', stats)