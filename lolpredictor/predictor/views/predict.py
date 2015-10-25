
from lolpredictor.predictor.models import *

from django.shortcuts import render
import logging
import pickle
from lolpredictor.predictor.traits.champion_played import store_champions_played
from lolpredictor.predictor.views.api import getSummonersByName, getCurrentGameBySummonerID
from lolpredictor.predictor.views.preprocessing import fill_missing_spots, sort_champion_list, \
    champion_played_to_features
import os
logger = logging.getLogger(__name__)


def predict(request):    
    print "Predicting !"
    if request.method == 'GET':
        return render(request, 'predictor/predictor.html')
    if request.method == 'POST':
        my_hash={}        
        summoner_name = request.POST["summoner_name"]       
        summoner_id = getSummonersByName(summoner_name)[summoner_name.lower()]["id"]
        print summoner_id
        game = getCurrentGameBySummonerID(summoner_id)        
        # Checks of game is ranked 5VS5
        if int(game["gameQueueConfigId"])!= 4:
            print 'Game not suited for this predictor.'
            return render(request, 'predictor/predictor.html')
        else : 
            winrate= parsegame(game,summoner_id)
            #makeprediction(inputvector)
        my_hash["winrate"] =  round(winrate,3)
    return render(request, 'predictor/predicted.html',my_hash)
def parsegame(game,current_summonner_id):
    participants = game["participants"]
    #used to determine wich team our summoner is on. 
    current_particpant = filter(lambda x: x['summonerId'] == current_summonner_id, participants)
    current_team = current_particpant[0]["teamId"]
    if current_team == 100:
        red = False
    team_1=[]
    team_2=[]

    for participant in participants:
        cp = store_champions_played(participant["summonerId"],participant["championId"]) 

        if participant["teamId"]== 100:
            participant
            team_1.append(cp)
        else:
            team_2.append(cp)


    #Sort champs  according to which place they are set   
    optimal_setup_1 = fill_missing_spots(sort_champion_list(team_1, []), team_1)
    optimal_setup_2 = fill_missing_spots(sort_champion_list(team_2, []), team_2)
    print "red: %s" % red
    print "team: %s" % team
    print optimal_setup_1
    print optimal_setup_2

    #Converts 
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

def makeprediction(inputvector):
    module_dir = os.path.dirname(__file__)
    print(module_dir)
    fileObject = open('networks/neuralHiddenNode5decay0.01','r')
    net = pickle.load(fileObject)
    net.sorted = False
    net.sortModules()
    return net.activate(inputvector)