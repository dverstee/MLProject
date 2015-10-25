from django.shortcuts import render
from lolpredictor.predictor.models import Summoner


def summoners(request):
    summoners = Summoner.objects.order_by('name')
    return render(request, 'predictor/summoners.html', {'summoners': summoners})