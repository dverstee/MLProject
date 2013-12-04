from django.shortcuts import render
from lolpredictor.predictor.models import Summoner, ChampionPlayed

def search(request):
    if 'sn' in request.GET and request.GET['sn']:
        summonerName = request.GET['sn']
        try:
            summoner = Summoner.objects.get(name=summonerName)
        except Summoner.DoesNotExist:
            return render(request, 'predictor/search.html', {'summoner': None, 'query': summonerName})
        championPlayed = ChampionPlayed.objects.filter(summoner=summoner).order_by('-nr_gameswithchamp')

        return render(request, 'predictor/search.html', {
            'summoner': summoner,
            'query': summonerName,
            'championPlayed': championPlayed
            })
    else:
        return render(request, 'predictor/search.html')