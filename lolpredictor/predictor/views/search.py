from django.shortcuts import render
from lolpredictor.predictor.models import Summoner

def search(request):
    if 'srch-term' in request.GET and request.GET['srch-term']:
        summonerName = request.GET['srch-term']
        summoner = None
        try:
            summoner = Summoner.objects.get(name=summonerName)
        except Summoner.DoesNotExist:
            pass
        return render(request, 'predictor/search.html', {'summoner': summoner, 'query': summonerName})
    else:
        return render(request, 'predictor/search.html')