from django.shortcuts import render
from api import *
from util import *
from django.db.models import Q
from datetime import timedelta
import globals

KEEP_CRAWLING_PERCENTAGE = 80



def crawler(request):
    if request.method == 'GET':
        return render(request, 'predictor/datacrawl.html')
    if request.method == 'POST':
        print "Getting Summoners"
        #bronze
        summoners = getSummonersByName("mani")
        id= summoners["mani"]["id"]
        recent_games = getRecentGamesById(id)   
        parse_ranked_games(recent_games,id)
        #silver      
        summoners = getSummonersByName("xindronke")
        id= summoners["xindronke"]["id"]
        recent_games = getRecentGamesById(id) 
        parse_ranked_games(recent_games,id)
        #gold
        summoners = getSummonersByName("Steeltje3")
        id= summoners["steeltje3"]["id"]
        recent_games = getRecentGamesById(id)   
        parse_ranked_games(recent_games,id)
        summoners = getSummonersByName("Tr1pzz")        
        id= summoners["tr1pzz"]["id"]
        recent_games = getRecentGamesById(id)   
        parse_ranked_games(recent_games,id)
        recrawl(0, 1)
        """
        summoners = getSummonersByName("batman")
        id= summoners["batman"]["id"]
        recent_games = getRecentGamesById(id)   
        parse_ranked_games(recent_games,id)"""
      
        """stats = getAggregatedStatsById(id) 
        for stat in stats:           
            print stat["id"] 
            startId =  int(request.POST["StartId"])

            """       

        """names = ["steeltje3","gezapigeeland","xindronke"]
        print ', '.join(names)        
        summoners = getSummonersByName(', '.join(names))
        print (summoners)
        ids = []
        for name in names:
            ids.append(summoners[name]["id"])     

        store_summoners(ids,"euw")"""
        """recent_games = getRecentGamesById(ids)   
        parse_ranked_games(recent_games,id)
        recrawl(0, 1)  """
        """store_summoner(id)"""

        """globals.nrgamesadded=0
        globals.nrerrors=0
        globals.nrofupdates=0
        startId =   id    
        nrofMatches =   int(request.POST["Range"]) 
        percentageadded = 10        
        while percentageadded < KEEP_CRAWLING_PERCENTAGE:
            for accountId in range(startId, startId + nrofMatches):
                recent_games = getRecentGamesById(accountId)       
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
        return render(request, 'predictor/success.html', my_hash)"""

def recrawler(request):
    recrawl(0,1)
    return render(request, 'predictor/success.html')

def recrawl(index, fragments):
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

    chosenSummoners = chosenSummoners[(len(chosenSummoners)/fragments)*index:(len(chosenSummoners)/fragments)*(index+1)]
    for summoner in chosenSummoners:
        print(summoner.account_id)
        try:
            recentGames = getRecentGamesById(summoner.account_id)
            if recentGames != None:
                matchesAdded = parse_ranked_games(recentGames, summoner.account_id)
            if matchesAdded != None:                        
                print "Matches added %s " % matchesAdded 
        except:
            print("other region.")



       
    return render(request, 'predictor/success.html')