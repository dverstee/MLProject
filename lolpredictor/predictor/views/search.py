from django.shortcuts import render
from lolpredictor.predictor.models import Summoner

def search(request):
    if request.method == 'GET':
        return render(request, 'predictor/search.html')

def search_post(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        books = Summoner.objects.filter(title__icontains=q)
        return render(request, 'search_results.html',
            {'books': books, 'query': q})

