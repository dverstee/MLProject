#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render

import logging
from  models import *
from api import *

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from datetime import *



logger = logging.getLogger(__name__)

nrofgameswitherror = 0
def index(request):
 	if request.method == 'GET':
		return render(request, 'predictor/index.html')
	if request.method == 'POST':

		name = request.POST["SummonerName"]
		print name
		summoner_id = getAccountIdByName(name)		
		most_played_champions = None
		if summoner_id:
			print summoner_id
			most_played_champions = getTopPlayedChampionsBySummonerId(summoner_id)
		if most_played_champions:
			my_hash = {}
			my_hash["most_played_champions"] = parseChampionlist(most_played_champions)
			my_hash["name"] = name
			print my_hash["most_played_champions"]
			return render(request, 'predictor/info.html', my_hash)
		else:
			return render(request, 'predictor/index.html')
def neural(request):	

	number_of_hidden_nodes = 1000
	number_of_training_epochs = 200
	#This is a dataset 
	#first argument is the dimension of the input
	# second argument is dimension of the output
	alldata = ClassificationDataSet(73, 1, nb_classes=2)
	

	matches = match.objects.all()
	print "Number of matches in db : " 
	print  len(matches)
	for matc in matches:	
		#s1 = Summoner.objects.filter( self.id() = )
		
		#todo nr of premades not correct yet ! And NR of wins ook niet!
		# als we willen kunnen we onderscheid maken tussen ranked of niet
		if matc.match_type == "RANKED_SOLO_5x5" :
			input = getDatafromMatch(matc)		
			alldata.addSample(input, matc.won)
		# if matc.match_type == "NORMAL" :
		# 	input = getDatafromMatch(matc)		
		# 	alldata.addSample(input, matc.won)
				
		
	tstdata, trndata = alldata.splitWithProportion( 0.25 )

	trndata._convertToOneOfMany( )
	tstdata._convertToOneOfMany( )			

	#First  arggument is number of  inputs.
	#Second argument is number of hidden nodes 
	#Third is number of outputs
	
	fnn = buildNetwork( trndata.indim, number_of_hidden_nodes, trndata.outdim, outclass=SoftmaxLayer )
	trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=False, weightdecay=0.01)
	trainer.trainEpochs(number_of_training_epochs)


	trnresult = percentError( trainer.testOnClassData(), trndata['class'] )
	tstresult = percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )

	print "epoch: %4d" %trainer.totalepochs
	print "  train error: %5.2f%%" %trnresult
	print "  test error: %5.2f%%" %tstresult
	my_hash = {}
	my_hash["tstresult"] = tstresult
	my_hash["trnresult"] = trnresult


	return render(request, 'predictor/neural.html' , my_hash )
def datacrawl(request):
	if request.method == 'GET':
		return render(request, 'predictor/datacrawl.html')
	if request.method == 'POST':

		startId = 		int(request.POST["StartId"])
		nrofMatches =	int(request.POST["Range"])	
	nrofMatchescrawled=0


	for accountId in range(startId, startId + nrofMatches):
		print accountId
		rg = getRecentGamesByAccountId(accountId)		
		if rg != None:
			matchesadded = parseRecentGames(rg,accountId)
			if matchesadded != None :
				nrofMatchescrawled = nrofMatchescrawled + matchesadded 
				print "Match added"
				print nrofMatchescrawled
		else :
			print "Error getting Recent Games"
	my_hash = {}
	my_hash["matchesadded"] = nrofMatchescrawled
	my_hash["error"] = nrofgameswitherror
	print nrofgameswitherror
	return render(request, 'predictor/success.html', my_hash)
def search_form(request):
	if request.method == 'GET':
		return render(request, 'predictor/search.html')

def search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
        books = Summoner.objects.filter(title__icontains=q)
        return render(request, 'search_results.html',
            {'books': books, 'query': q})


def parseChampionlist(champions):
	parsed_list = []
	for key, champion in champions.items():
		champion_hash = {}
		champion_hash["id"] = champion["championId"]
		champion_hash["games"] = champion["totalGamesPlayed"]
		champion_hash["image"] = "https://github.com/rwarasaurus/league-of-legends-database/blob/master/icons/%d.jpg?raw=true" % champion["championId"]
		parsed_list.append(champion_hash)
	return parsed_list

def parseRecentGames(games, accountid):

	nrrecentrankedgames = 0
	nrrecentnormalgames = 0	
	for game in games:		

		if game["queueType"] == "RANKED_SOLO_5x5" :
			print "Storing Ranked game" 
			m = storeMatch(game,"RANKED_SOLO_5x5",accountid)
			if m != None :
				nrrecentrankedgames = nrrecentrankedgames + 1
			else :
				nrofgameswitherror = nrofgameswitherror + 1 
		if game["queueType"] == "NORMAL" :			
			if game["level"] == "30" :
				nrrecentnormalgames = nrrecentnormalgames + 1
				print "Storing Normal game lvl 30" 
				m = storeMatch(game,"NORMAL",accountid)
				m = storeMatch(game,"RANKED_SOLO_5x5",accountid)
				if m != None :
					nrrecentnormalgames = nrrecentnormalgames + 1
				else :
					nrofgameswitherror = nrofgameswitherror + 1 


	if nrrecentrankedgames == 0 and nrrecentnormalgames ==0 :
		logger.debug("Not enough matches")
		return None	
	#recentwinpercentage = float(nrrecentrankedgameswon) / float(nrrecentrankedgames) * 100
	
	#print recentwinpercentage

	#TODO : SELECT MOST RECENT MATCH !!!! 


	return nrrecentrankedgames + nrrecentnormalgames
def storeMatch(game , type ,accountid):
	#Store yourself
	print "Store Myself"
	our_team = []
	their_team = []
	championid = game["championId"]
	summoner_id = game["summonerId"]
	teamid = game["teamId"]
	print championid
	print summoner_id
	print teamid
	if summoner_id == 0:
		summoner_id = getSummonerIdByAccountId(accountid)
	print summoner_id
	summoner = StoreSummonerandChampion(accountid, championid,summoner_id)
	if summoner == None:
			return None
	our_team.append(summoner)
	
	#Store Others$
	print "Store Others"
	fellowplayers = game["fellowPlayers"]["array"]
	for player in fellowplayers:	
		champid = player["championId"]	
		summoner_id = player["summonerId"]	

		accountId = getAccountIdBySummonerId(summoner_id)	
		summoner = StoreSummonerandChampion(accountId, champid,summoner_id)
		if summoner == None:
			return None
		if player ["teamId"] == teamid : 
			our_team.append(summoner)
		else :
			their_team.append(summoner)

	if 	teamid == 100:
		team1_is_red = True
	else:	
		team1_is_red = False
	#TODO : PREMADE size uitzoeken hoe het werkt.
	premadesize = game["premadeSize"]

	won = determineWin(game)

	if 	won == 1:
		win = True
	else:	
		win = False
	#TODO Iterate over the list to make the match object ! :) 
	m = match.objects.create(team1_is_red=team1_is_red,nr_premade_team1=premadesize,nr_premade_team2=premadesize,won=win,team_1summoner1_id=our_team[0],team_1summoner2_id=our_team[1],team_1summoner3_id=our_team[2],team_1summoner4_id=our_team[3],team_1summoner5_id=our_team[4],team_2summoner1_id=their_team[0],team_2summoner2_id=their_team[1],team_2summoner3_id=their_team[2],team_2summoner4_id=their_team[3],team_2summoner5_id=their_team[4],match_type=type)
	return m
def StoreSummonerandChampion(accountId , championId, summoner_id)	:

	accountstats = getAggregatedStatsByAccountID(accountId)
	

	totalGamesPlayed =  0
	totalGamesWon = 0 
	for stat in accountstats:	
		champId = stat["championId"]
		if champId == championId:
			if stat["statType"] == "TOTAL_SESSIONS_WON":
				totalGamesWon =  stat["value"]
			if stat["statType"] == "TOTAL_SESSIONS_PLAYED":
				totalGamesPlayed =  stat["value"]


	c1 = ChampionPlayed.objects.create(nr_gameswithchamp=totalGamesPlayed,nr_gameswonwithchamp=totalGamesWon,champid = championId)
	c1.save()
	#Build the summoner
	
	league = getLeagueForPlayerBySummonerID(summoner_id)	
	if league==None :
		return None
	rank = league["requestorsRank"]
	tier = league["tier"]
	name = league["requestorsName"]	
	league = league["entries"]["array"]	
		
	print name	
	print tier

	for player in league:	
			pn = player["playerOrTeamName"]
			if pn == name :								
				lp =  player["leaguePoints"]
				hotstreak = player["hotStreak"]
				if hotstreak == "false":
					recentwinpercentage =33.0
				else:					
					recentwinpercentage =80.0
				break
	
	rank=ranktoint(rank) 
	s1 = Summoner.objects.create(champion_played=c1 ,leaguepoints=lp ,tier=str(tier) ,rank=rank  ,recentwinpercentage=recentwinpercentage ) 
	s1.save()	
	return s1	
def ranktoint(rank):
	if rank == "I":
		return 1	
	elif rank == "II":
		return 2
	elif rank == "III":
	 return 3
	elif rank == "IV":
		return 4
	elif rank == "V":
		return 5  
def tiertoint(tier):
	if tier == "BRONZE":
		return 1	
	elif tier == "SILVER":
		return 2
	elif tier == "GOLD":
	 return 3
	elif tier == "PLATINUM":
		return 4
	elif tier == "DIAMOND":
		return 5  
def determineWin (game):
	stats =  game["statistics"]["array"]
	for stat in stats :
		win = stat["statType"]
		if win == "WIN" :
			return stat["value"]

def getDatafromMatch(matc):
	input=[]

	tier11 = tiertoint(matc.team_1summoner1_id.tier)
	tier12 = tiertoint(matc.team_1summoner2_id.tier)
	tier13 = tiertoint(matc.team_1summoner3_id.tier)
	tier14 = tiertoint(matc.team_1summoner4_id.tier)
	tier15 = tiertoint(matc.team_1summoner5_id.tier)
	tier21 = tiertoint(matc.team_2summoner1_id.tier)
	tier22 = tiertoint(matc.team_2summoner2_id.tier)
	tier23 = tiertoint(matc.team_2summoner3_id.tier)
	tier24 = tiertoint(matc.team_2summoner4_id.tier)
	tier25 = tiertoint(matc.team_2summoner5_id.tier)



	matchinput =  [ matc.team1_is_red , matc.nr_premade_team1, matc.nr_premade_team2 ] 
	summoner11input = [ matc.team_1summoner1_id.champion_played.nr_gameswithchamp , matc.team_1summoner1_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner1_id.champion_played.champid,
	matc.team_1summoner1_id.leaguepoints , tier11 , matc.team_1summoner1_id.rank  , matc.team_1summoner1_id.recentwinpercentage ]
		
	summoner12input = [ matc.team_1summoner2_id.champion_played.nr_gameswithchamp , matc.team_1summoner2_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner2_id.champion_played.champid,
	matc.team_1summoner2_id.leaguepoints , tier12 , matc.team_1summoner2_id.rank  , matc.team_1summoner2_id.recentwinpercentage ]

	summoner13input = [ matc.team_1summoner3_id.champion_played.nr_gameswithchamp , matc.team_1summoner3_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner3_id.champion_played.champid,
	matc.team_1summoner3_id.leaguepoints , tier13 , matc.team_1summoner3_id.rank  , matc.team_1summoner3_id.recentwinpercentage ]

	summoner14input = [ matc.team_1summoner4_id.champion_played.nr_gameswithchamp , matc.team_1summoner4_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner4_id.champion_played.champid,
	matc.team_1summoner4_id.leaguepoints , tier14, matc.team_1summoner3_id.rank  , matc.team_1summoner4_id.recentwinpercentage ]

	summoner15input = [ matc.team_1summoner5_id.champion_played.nr_gameswithchamp , matc.team_1summoner5_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner5_id.champion_played.champid,
	matc.team_1summoner5_id.leaguepoints , tier15 , matc.team_1summoner5_id.rank  , matc.team_1summoner5_id.recentwinpercentage ]

	summoner21input = [ matc.team_2summoner1_id.champion_played.nr_gameswithchamp , matc.team_2summoner1_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner1_id.champion_played.champid,
	matc.team_2summoner1_id.leaguepoints , tier21 , matc.team_2summoner1_id.rank  , matc.team_2summoner1_id.recentwinpercentage ]
		
	summoner22input = [ matc.team_2summoner2_id.champion_played.nr_gameswithchamp , matc.team_2summoner2_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner2_id.champion_played.champid,
	matc.team_2summoner2_id.leaguepoints , tier22 , matc.team_2summoner2_id.rank  , matc.team_2summoner2_id.recentwinpercentage ]

	summoner23input = [ matc.team_2summoner3_id.champion_played.nr_gameswithchamp , matc.team_2summoner3_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner3_id.champion_played.champid,
	matc.team_2summoner3_id.leaguepoints , tier23 , matc.team_2summoner3_id.rank  , matc.team_2summoner3_id.recentwinpercentage ]

	summoner24input = [ matc.team_2summoner4_id.champion_played.nr_gameswithchamp , matc.team_2summoner4_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner4_id.champion_played.champid,
	matc.team_2summoner4_id.leaguepoints , tier24, matc.team_2summoner3_id.rank  , matc.team_2summoner4_id.recentwinpercentage ]

	summoner25input = [ matc.team_2summoner5_id.champion_played.nr_gameswithchamp , matc.team_2summoner5_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner5_id.champion_played.champid,
	matc.team_2summoner5_id.leaguepoints , tier25 , matc.team_2summoner5_id.rank  , matc.team_2summoner5_id.recentwinpercentage ]


	input.extend(matchinput)
	input.extend(summoner11input)
	input.extend(summoner12input)
	input.extend(summoner13input)
	input.extend(summoner14input)
	input.extend(summoner15input)
	input.extend(summoner21input)
	input.extend(summoner22input)
	input.extend(summoner23input)
	input.extend(summoner24input)
	input.extend(summoner25input)
	
	return input