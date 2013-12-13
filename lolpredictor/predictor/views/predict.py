from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer, BiasUnit
from pybrain.structure           import FullConnection, FeedForwardNetwork, LinearLayer, SigmoidLayer
from api import *
from util import *
from preprocessing import *
from neural import *
from lolpredictor.predictor.models import *

from django.shortcuts import render
import itertools, collections
import logging
import pickle

import globals
logger = logging.getLogger(__name__)


def predict(request):    
    print "Predicting !"
    if request.method == 'GET':
        return render(request, 'predictor/predictor.html')
    if request.method == 'POST':
        summoner_name = str(request.POST["summoner_name"])
        print summoner_name 
        game = retrieveInProgressSpectatorGameInfo(summoner_name)
        if game["queueTypeName"]!="RANKED_SOLO_5x5":
            print 'Game not suited for this predictor.'
            return render(request, 'predictor/predictor.html')
        else : 
            parsegame(game)
            #makeprediction(inputvector)
       
    return render(request, 'predictor/predictor.html')
      
       
def parsegame(game):
    print game
    #used to determine wich team our summoner is on.
    pick_turn_our_summoner = game["pickTurn"]
    team = 2
    champ_hash = makechamphash(game)
    team_1 = []
    teamOne = game["teamOne"]["array"]
    for summoner in teamOne:
        account_id = summoner["accountId"]
        summoner_id = summoner["summonerId"]
        internalname = summoner["summonerInternalName"]
        champion_id = champ_hash[internalname]
        pick_turn = summoner["pickTurn"]
        #No overhead in storing summoner 
        summoner = store_summoner(summoner_id,account_id)
        #there is overhead in store_championplayed, avoid this by new function.        
        cp = makeChampionplayed(account_id,summoner,champion_id)        
        team_1.append(cp)
        if pick_turn == pick_turn_our_summoner:
            team = 1
    team_2 = []
    teamTwo = game["teamTwo"]["array"]
    for summoner in teamTwo:
        account_id = summoner["summonerId"]
        summoner_id = summoner["accountId"]
        internalname = summoner["summonerInternalName"]
        champion_id = champ_hash[internalname]
        #No overhead in storing summoner 
        summoner = store_summoner(account_id,summoner_id)
        #there is overhead in store_championplayed, avoid this by new function.        
        cp = makeChampionplayed(account_id,summoner,champion_id)        
        team_2.append(cp)
    #Sort champs     
    optimal_setup_1 = fill_missing_spots(sort_champion_list(team_1, []), team_1)
    optimal_setup_2 = fill_missing_spots(sort_champion_list(team_2, []), team_2)
    print team
    print optimal_setup_1
    print optimal_setup_2
    feature = getDatafromMatch(optimal_setup_1, optimal_setup_2, True)
    print feature
    print makeprediction(feature)
    feature = getDatafromMatch(optimal_setup_2, optimal_setup_1, False)
    print feature
    print makeprediction(feature)


def getDatafromMatch(team_1, team_2, team1IsRed):
    input = matchups_win_rate(team_1,team_2)
    for s in team_1:        
        input += champion_played_to_features(s)
    for s in team_2:
        input += champion_played_to_features(s)

    if team1IsRed:
        input += [1, 0]
    else:
        input += [0, 1]   
    return input


def matchups_win_rate(team_1,team_2):   
    win_rates = []
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


def makeChampionplayed(account_id, summoner,champion_id):  
    champion = Champion.objects.get(pk=champion_id)   
    try:
        cp = ChampionPlayed.objects.get(summoner=summoner,champion=champion)
        if cp is not None:
            print_champion_played(summoner,False)
            return cp
    except:     
        pass
    accountstats = getAggregatedStatsByAccountID(account_id)
    champion = Champion.objects.get(pk=champion_id)    
    param_hash = {}
    param_hash["champion"] = champion
    param_hash["summoner"] = summoner
    print param_hash
    
    for champion_stats in accountstats:
        champion_id = champion_stats["championId"]
        # Only store the relevant
        if champion_id == champion.key:
            statType = champion_stats["statType"]
            if statType == "TOTAL_SESSIONS_PLAYED":                
                param_hash["nr_gameswithchamp"] =  champion_stats["value"]
            if statType == "TOTAL_ASSISTS":                
                param_hash["average_assists"] =  champion_stats["value"]                
            if statType == "TOTAL_DEATHS_PER_SESSION":               
                param_hash["average_deaths"] =  champion_stats["value"]
            if statType == "TOTAL_CHAMPION_KILLS":
                param_hash["average_kills"] =  champion_stats["value"]
            if statType == "TOTAL_GOLD_EARNED":
                param_hash["average_gold"] =  champion_stats["value"]
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
    fileObject = open('prettygood80decay0.01withoutRB','r')
    net = pickle.load(fileObject)
   
    return net.activate(inputvector)