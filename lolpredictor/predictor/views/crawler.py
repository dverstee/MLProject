from django.shortcuts import render
from api import *
from util import *
from django.db.models import Q
import globals

KEEP_CRAWLING_PERCENTAGE = 80

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
                    if matchesadded != None:                        
                        print "Matches added %s " % matchesadded                      
                else :
                    print "Error getting Recent Games"
            
            
            if globals.nrgamesadded + globals.nrerrors == 0 :
                print "Inrease range. No games were found"
                break 
            percentageadded=globals.nrgamesadded/(globals.nrgamesadded + globals.nrerrors)*100
            print "Percentage of possible games added %s " % (percentageadded)
        my_hash = {}
        my_hash["matchesadded"] = globals.nrgamesadded
        my_hash["error"] = globals.nrerrors
        my_hash["updated"] = globals.nrofupdates
        return render(request, 'predictor/success.html', my_hash)

def recrawler(request):
    recrawl()
    return render(request, 'predictor/success.html')

def recrawl():
    summoners = Summoner.objects.all()
    chosenSummoners = []
    print 'Summoner filtering start.'
    for summoner in summoners:
        matchCount = Match.objects.filter(
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
            ).count()
        if matchCount < 3:
            chosenSummoners.append(summoner)
    print 'Summoner filtering completed. ' + str(len(chosenSummoners)) + ' summoners selected.'

    for summoner in chosenSummoners:
        recentGames = getRecentGamesByAccountId(summoner.account_id)
        if recentGames != None:
            matchesAdded = parse_ranked_games(recentGames, summoner.account_id)
            if matchesAdded != None:                        
                print "Matches added %s " % matchesAdded
    return render(request, 'predictor/success.html')