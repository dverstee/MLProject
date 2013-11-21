#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
import json
import unirest
import logging
import codecs
import re
from  models import *

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.datasets 			 import SupervisedDataSet
from django.http 				import HttpResponse
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
from datetime import *



logger = logging.getLogger(__name__)


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
	print "hallo"

	number_of_hidden_nodes = 20 
	number_of_training_epochs = 20
	#This is a dataset 
	#first argument is the dimension of the input
	# second argument is dimension of the output
	

	means = [(-1,0),(2,4),(3,1)]
	cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7])]
	alldata = ClassificationDataSet(2, 1, nb_classes=3)
	for n in xrange(400):
	    for klass in range(3):
	        input = multivariate_normal(means[klass],cov[klass])
	        alldata.addSample(input, [klass])

	tstdata, trndata = alldata.splitWithProportion( 0.25 )

	trndata._convertToOneOfMany( )
	tstdata._convertToOneOfMany( )

	matches = match.objects.all()
	for matc in matches:	
		#s1 = Summoner.objects.filter( self.id() = )
		ids = matc.team_1summoner1_id.id
		print ids
		print matc.team_1summoner1_id.rank
	
		print matc.team_1summoner1_id.leaguepoints
		
		
				

	

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

	startId = 27124075
	nrofMatches = 1000
	nrofMatchescrawled=0
	for accountId in range(startId, startId + nrofMatches):
		print accountId
		rg = getRecentGamesByAccountId(accountId)		
		if rg != None:
			info = parseRecentGames(rg,accountId)
			if info !=None :
				nrofMatchescrawled = nrofMatchescrawled +1 
				print "Match added"
	print info
	return HttpResponse("hi")

def parseChampionlist(champions):
	parsed_list = []
	for key, champion in champions.items():
		champion_hash = {}
		champion_hash["id"] = champion["championId"]
		champion_hash["games"] = champion["totalGamesPlayed"]
		champion_hash["image"] = "https://github.com/rwarasaurus/league-of-legends-database/blob/master/icons/%d.jpg?raw=true" % champion["championId"]
		parsed_list.append(champion_hash)
	return parsed_list
def parseRecentGames(recentGames, accountid):

	games = recentGames["gameStatistics"]["array"]	
	nrrecentrankedgames = 0
	nrrecentrankedgameswon = 0
	for game in games:		

		if game["queueType"] == "RANKED_SOLO_5x5" :			
			nrrecentrankedgames = nrrecentrankedgames + 1 
			win = determineWin(game)
			if win == 1 :
				nrrecentrankedgameswon = nrrecentrankedgameswon +1 
				
	if nrrecentrankedgames ==0 :
		print "Not enough Ranked matches"  
		return None	
	recentwinpercentage = float(nrrecentrankedgameswon) / float(nrrecentrankedgames) * 100
	print nrrecentrankedgames
	print recentwinpercentage

	#TODO : SELECT MOST RECENT MATCH !!!! 

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
	match.objects.create(team1_is_red=team1_is_red,nr_premade_team1=premadesize,nr_premade_team2=premadesize,won=win,team_1summoner1_id=our_team[0],team_1summoner2_id=our_team[1],team_1summoner3_id=our_team[2],team_1summoner4_id=our_team[3],team_1summoner5_id=our_team[4],team_2summoner1_id=their_team[0],team_2summoner2_id=their_team[1],team_2summoner3_id=their_team[2],team_2summoner4_id=their_team[3],team_2summoner5_id=their_team[4])
		
	return summoner_id
def StoreSummonerandChampion(accountId , championId, summoner_id)	:

	print accountId
	accountstats = getAggregatedStatsByAccountID(accountId)
	accountstats = accountstats["lifetimeStatistics"]["array"]

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
				break
	recentwinpercentage =50.0
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
def determineWin (game):
	stats =  game["statistics"]["array"]
	for stat in stats :
		win = stat["statType"]
		if win == "WIN" :
			return stat["value"]
def getSummonerIdByAccountId(AccountId):	
	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getAllPublicSummonerDataByAccount/%s" % AccountId,
	headers={
    	"X-Mashape-Authorization": "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"
  	});
  	values = json.loads(response.raw_body)  
  	sumid = values["summoner"]["sumId"]

  	
  	return sumid
def getAccountIdBySummonerId(summonerid):
	print summonerid
	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getSummonerBySummonerId/%s" % summonerid,
	headers={
    	"X-Mashape-Authorization": "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"
  	});
  	values = json.loads(response.raw_body)  
  	values = values["array"]

  	for namez in values:  		
  		name = namez
  	
  	accountid =	getAccountIdByName(name)
  	 
  	return accountid
def getAccountIdByName(name):
  	name = name.replace(' ', '')  
  	name = unicode_conversion(name);
 	print name
 	url = u"https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getSummonerByName/"
 	url = url + name 	
 	url = url.encode('utf-8')
	response = unirest.get(url,
	headers={
    	"X-Mashape-Authorization": "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"
  	},
  	encoding='utf-8');

 	values = json.loads(response.raw_body)	
  	if 'acctId' in values:
  		return values['acctId']
  	return None
def getInfoByaccountId(accountId):
   	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getAllPublicSummonerDataByAccount/%s" % accountId,
	headers={
		"X-Mashape-Authorization": "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"
		});
	values = json.loads(response.raw_body)	
	if values:
		return values
	return None
def getTopPlayedChampionsBySummonerId(accountId):
	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUNE/summoner/retrieveTopPlayedChampions/%s" % accountId,
	headers={
		"X-Mashape-Authorization": "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"
		});
	values = json.loads(response.raw_body)

	if values:
		return values
	return None
def getRecentGamesByAccountId(accountId):
	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getRecentGames/%s" % accountId,
	headers={
		"X-Mashape-Authorization": "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"
		});
	values = json.loads(response.raw_body)

	if values:
		return values
	return None
def getAggregatedStatsByAccountID(accountId):
	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getAggregatedStats/%s" % accountId,
	headers={
		"X-Mashape-Authorization": "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"
		});
	values = json.loads(response.raw_body)

	if values:
		return values
	return None
def getLeagueForPlayerBySummonerID(SummonerID):
	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getLeagueForPlayer/%s" % SummonerID,
	headers={
		"X-Mashape-Authorization": "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"
		});
	values = json.loads(response.raw_body)
	
	try:
		error = values['requestorsRank']
		return values
	except KeyError:
		print "Weird Error"
		return None
def unicode_conversion(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import htmlentitydefs
            entity = htmlentitydefs.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return unicode(entity, "iso-8859-1")
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)


