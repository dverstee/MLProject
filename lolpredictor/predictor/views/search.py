from django.shortcuts import render
from django.db.models import Avg
from django.db.models import Q
from lolpredictor.predictor.models import Summoner, ChampionPlayed, Match

def search(request):
    if 'sn' in request.GET and request.GET['sn']:
        summonerName = request.GET['sn']
        try:
            summoner = Summoner.objects.get(name=summonerName)
        except Summoner.DoesNotExist:
            return render(request, 'predictor/search.html', {'summoner': None, 'query': summonerName})

        championPlayed = ChampionPlayed.objects.filter(summoner=summoner).order_by('-nr_gameswithchamp')
        stats = ChampionPlayed.objects.values('champion').annotate(
            average_kills=Avg('average_kills'),
            average_deaths=Avg('average_deaths'),
            average_assists=Avg('average_assists'),
            average_gold=Avg('average_gold'),
            )
        championStats = {}
        for stat in stats:
            championStats[stat['champion']] = {
                'average_kills':stat['average_kills'],
                'average_deaths':stat['average_deaths'],
                'average_assists':stat['average_assists'],
                'average_gold':stat['average_gold']
                }
        matches = Match.objects.filter(
            Q(team_1summoner1_id__summoner=summoner) |
            Q(team_1summoner2_id__summoner=summoner) |
            Q(team_1summoner3_id__summoner=summoner) |
            Q(team_1summoner4_id__summoner=summoner) |
            Q(team_1summoner5_id__summoner=summoner) |
            Q(team_2summoner1_id__summoner=summoner) |
            Q(team_2summoner2_id__summoner=summoner) |
            Q(team_2summoner3_id__summoner=summoner) |
            Q(team_2summoner4_id__summoner=summoner) |
            Q(team_2summoner5_id__summoner=summoner)
            )

        return render(request, 'predictor/search.html', {
            'summoner': summoner,
            'query': summonerName,
            'championPlayed': championPlayed,
            'championStats': championStats,
            'matches': matches,
            })
    else:
        return render(request, 'predictor/search.html')