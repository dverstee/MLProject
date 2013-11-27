from django.shortcuts import render
from api import *
from util import *
import globals

KEEP_CRAWLING_PERCENTAGE =80
def crawler(request):
    if request.method == 'GET':
        return render(request, 'predictor/datacrawl.html')
    if request.method == 'POST':
        globals.nrgamesadded=0
        globals.nrerrors=0
        globals.nrofupdates=0
        startId =       int(request.POST["StartId"])
        nrofMatches =   int(request.POST["Range"])  
                 
        percentageadded = 10        
        while percentageadded < KEEP_CRAWLING_PERCENTAGE:
            for accountId in range(startId, startId + nrofMatches):
                recent_games = getRecentGamesByAccountId(accountId)       
                if recent_games != None:
                    matchesadded = parse_ranked_games(recent_games,accountId)
                    if matchesadded != None :                        
                        print "Matches added %s " % matchesadded                      
                else :
                    print "Error getting Recent Games"
            
            
            if globals.nrgamesadded + globals.nrerrors == 0 :
                print "Inrease range no Games were found"
                break 
            percentageadded=globals.nrgamesadded/(globals.nrgamesadded + globals.nrerrors)*100
            print "Percentage of possible games added %s " % (percentageadded)
        my_hash = {}
        my_hash["matchesadded"] = globals.nrgamesadded
        my_hash["error"] = globals.nrerrors
        my_hash["updated"] = globals.nrofupdates
        return render(request, 'predictor/success.html', my_hash)