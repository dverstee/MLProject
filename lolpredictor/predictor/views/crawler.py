from django.shortcuts import render
from api import *
from util import *
def crawler(request):
    if request.method == 'GET':
        return render(request, 'predictor/datacrawl.html')
    if request.method == 'POST':

        startId =       int(request.POST["StartId"])
        nrofMatches =   int(request.POST["Range"])  
        nrofMatchescrawled=0     
      


        for accountId in range(startId, startId + nrofMatches):
            recent_games = getRecentGamesByAccountId(accountId)       
            if recent_games != None:
                matchesadded = parse_ranked_games(recent_games,accountId)
                if matchesadded != None :
                    nrofMatchescrawled = nrofMatchescrawled + matchesadded 
                    print "Match added"
                    print nrofMatchescrawled
            else :
                print "Error getting Recent Games"
        my_hash = {}
        my_hash["matchesadded"] = nrofMatchescrawled
        my_hash["error"] = 0
        return render(request, 'predictor/success.html', my_hash)