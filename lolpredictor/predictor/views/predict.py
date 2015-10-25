
from lolpredictor.predictor.models import *

from django.shortcuts import render
import logging
import pickle
from lolpredictor.predictor.traits.summoner import store_summoners
from lolpredictor.predictor.utils.formatting import print_champion_played
from lolpredictor.predictor.views.api import retrieveInProgressSpectatorGameInfo, getAggregatedStatsById
from lolpredictor.predictor.views.preprocessing import champion_played_to_features, fill_missing_spots, \
    sort_champion_list
import os
import globals
logger = logging.getLogger(__name__)


def predict(request):    
    print "Predicting !"
    if request.method == 'GET':
        return render(request, 'predictor/predictor.html')
    if request.method == 'POST':
        my_hash={}
        
        summoner_name = request.POST["summoner_name"]
        print summoner_name 
      
        game = retrieveInProgressSpectatorGameInfo(summoner_name)
        print game
        if game["game"]["queueTypeName"]!="RANKED_SOLO_5x5":
            print 'Game not suited for this predictor.'
            return render(request, 'predictor/predictor.html')
        else : 
            winrate= parsegame(game)
            #makeprediction(inputvector)
        my_hash["winrate"] =  round(winrate,3)

    return render(request, 'predictor/predicted.html',my_hash)
def parsegame(game):
    
    #used to determine wich team our summoner is on.
    accountid_our_summoner = game["playerCredentials"]["playerId"]
    game = game['game']     
    red = True
    team = 2
    champ_hash = makechamphash(game)
    team_1 = []
    team_1_summonerIds = []
    team_2 = []    
    team_2_summonerIds = []
    teamOne = game["teamOne"]["array"]
    teamTwo = game["teamTwo"]["array"]
    for summoner in teamOne:
      team_1_summonerIds.append(summoner["summonerId"])
    for summoner in teamTwo:
      team_2_summonerIds.append(summoner["summonerId"])

    all_ids=team_1_summonerIds + team_2_summonerIds    
    store_summoners(all_ids,globals.REGION)

    for summoner in teamOne:      
        summoner_id = summoner["summonerId"]
        internalname = summoner["summonerInternalName"]
        champion_id = champ_hash[internalname]      
        #there is overhead in store_championplayed , avoid this by new function.        
        cp = makeChampionplayed(summoner_id,champion_id) 
        account_id = summoner["accountId"]       
        team_1.append(cp)
        if accountid_our_summoner == account_id:
            team = 1
            red= False
  
    for summoner in teamTwo:        
        summoner_id = summoner["summonerId"]
        internalname = summoner["summonerInternalName"]
        champion_id = champ_hash[internalname]      
        #there is overhead in store_championplayed , avoid this by new function.        
        cp = makeChampionplayed(summoner_id,champion_id) 
        team_2.append(cp)
    #Sort champs     
    optimal_setup_1 = fill_missing_spots(sort_champion_list(team_1, []), team_1)
    optimal_setup_2 = fill_missing_spots(sort_champion_list(team_2, []), team_2)
    print "red: %s" % red
    print "team: %s" % team
    print optimal_setup_1
    print optimal_setup_2
    feature = getDatafromMatch(optimal_setup_1, optimal_setup_2, True, red)   
    pred1= makeprediction(feature)
    feature = getDatafromMatch(optimal_setup_1, optimal_setup_2, False, red)
    pred2 = makeprediction(feature)
    winrate = float(pred1[0]+pred2[1])/float(2.0)

    return winrate*100

def getDatafromMatch(team_1,team_2,reverse,red):
    input = matchups_win_rate(team_1,team_2,reverse)
    if not reverse:
        for s in team_1:        
            input += champion_played_to_features(s)
        for s in team_2:
            input += champion_played_to_features(s)
    else:
        for s in team_2:        
            input += champion_played_to_features(s)
        for s in team_1:
            input += champion_played_to_features(s)

    if (red and not reverse) or (not red and reverse):
        input += [1, 0]
    else:
        input += [0, 1] 
    return input


def matchups_win_rate(team_1,team_2,reverse): 
    win_rates = []
    if not reverse:
        team_temp = team_1
        team_1=team_2
        team_2=team_temp

    for i in range(len(team_1)):
        try:
            matchup = Matchup.objects.get(champion_1=team_1[i].champion, champion_2=team_2[i].champion)
            win_rates.append(matchup.win_rate)
        except:
            win_rates.append(0.5)
    synergys = []
    try:
        synergys.append(Synergy.objects.get(champion_1=team_1[3].champion, champion_2=team_1[4].champion).win_rate)
    except:
        synergys.append(0.5)
    try:
        synergys.append(1 - Synergy.objects.get(champion_1=team_2[3].champion, champion_2=team_2[4].champion).win_rate)
    except:
        synergys.append(0.5)
    return win_rates + synergys


def makechamphash(match):
    champ_hash = {} 
    champs = match["playerChampionSelections"]["array"]
    for champ in champs:
        champ_hash[champ["summonerInternalName"]]=champ["championId"]
    return champ_hash


def makeChampionplayed(summoner_id,champion_id):

    try:
        print(champion_id)
        champion = Champion.objects.get(pk=champion_id) 
        summoner = Summoner.objects.get(summoner_id=summoner_id)
        cp = ChampionPlayed.objects.get(summoner=summoner,champion=champion)
        if cp is not None:
            print_champion_played(summoner,False)
            return cp
    except:     
        pass
    try:
        accountstats = getAggregatedStatsById(summoner_id)
        accountstats = accountstats["champions"]
    except:
        print accountstats



    champion = Champion.objects.get(pk=champion_id)    
    param_hash = {}
    param_hash["champion"] = champion
    param_hash["summoner"] = summoner
    
    for champion_stats in accountstats:
        champion_id = champion_stats["id"]
        # Only store the relevant
        if champion_id == champion.key:
                stats = champion_stats["stats"]     
        
                param_hash["nr_gameswithchamp"] = stats["totalSessionsPlayed"]
                param_hash["average_assists"] = stats["totalAssists"]
                param_hash["average_deaths"] = stats["totalDeathsPerSession"]
                param_hash["average_kills"] = stats["totalChampionKills"]
                param_hash["average_gold"] = stats["totalGoldEarned"]
    try :
        param_hash["average_assists"] = param_hash["average_assists"] / param_hash["nr_gameswithchamp"]
        param_hash["average_deaths"] = param_hash["average_deaths"] / param_hash["nr_gameswithchamp"]
        param_hash["average_kills"] = param_hash["average_kills"] / param_hash["nr_gameswithchamp"]
        param_hash["average_gold"] = param_hash["average_gold"] / param_hash["nr_gameswithchamp"]
    except KeyError :
        param_hash["nr_gameswithchamp"] = 1
        param_hash["average_assists"] = 0
        param_hash["average_deaths"] = 1
        param_hash["average_kills"] = 1
        param_hash["average_gold"] = 2000

    c1 = ChampionPlayed.objects.create(**param_hash)
    print_champion_played(summoner,True)
    return c1


def makeprediction(inputvector):
    module_dir = os.path.dirname(__file__)
    print(module_dir)
    fileObject = open('networks/neuralHiddenNode5decay0.01','r')
    net = pickle.load(fileObject)
    net.sorted = False
    net.sortModules()
    return net.activate(inputvector)