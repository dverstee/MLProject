#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from  lolpredictor.predictor.models import *
from datetime import *
from api import *
from django.db import IntegrityError
logger = logging.getLogger(__name__)

REFRESH_SUMMONER_INTERVAL = 3600*24 # One day refresh interval

def parse_champions(champions):
	parsed_list = []
	for key, champion in champions.items():
		champion_hash = {}
		champion_hash["id"] = champion["championId"]
		champion_hash["games"] = champion["totalGamesPlayed"]
		champion_hash["image"] = "https://github.com/rwarasaurus/league-of-legends-database/blob/master/icons/%d.jpg?raw=true" % champion["championId"]
		parsed_list.append(champion_hash)
	return parsed_list

def parse_ranked_games(games, accountid):

	nrrecentrankedgames = 0
	nrrecentnormalgames = 0	
	for game in games:		
		if game["queueType"] == "RANKED_SOLO_5x5" :
			print "Storing Ranked game" 
			m = store_match(game,"RANKED_SOLO_5x5",accountid)
	if nrrecentrankedgames == 0 and nrrecentnormalgames ==0 :
		logger.debug("Not enough matches")
		return None	
	return nrrecentrankedgames + nrrecentnormalgames

def store_match(game , type ,account_id):
	our_team = []
	their_team = []
	championid = game["championId"]
	summoner_id = getSummonerIdByAccountId(account_id)
	teamid = game["teamId"]

	if summoner_id is None:
		return None
	try:
		summoner = Summoner.objects.get(pk=account_id)
	except:
		summoner = None
	# Check if this summoner has been updated recently
	if not summoner or datetime.now() - summoner.updated_at.replace(tzinfo=None) > timedelta(seconds=REFRESH_SUMMONER_INTERVAL):
		summoner = store_summoner(summoner_id, account_id)
		if summoner == None:
			return None
		store_champions_played(account_id)
	
	champion = Champion.objects.get(pk=championid)
	if champion is None:
		return None
	champPlayed=ChampionPlayed.objects.get(summoner = summoner, champion=champion )		
	our_team.append(champPlayed)
	
	#Store Others
	fellowplayers = game["fellowPlayers"]["array"]
	for player in fellowplayers:	
		champion_id = player["championId"]	
		summoner_id = player["summonerId"]	

		accountId = getAccountIdBySummonerId(summoner_id)	
		summoner = store_summoner(summoner_id, accountId)
		champion = Champion.objects.get(pk=champion_id)
		if summoner:
			store_champions_played(accountId)
		else:
			return None
		champion_played = ChampionPlayed.objects.get(summoner = summoner, champion=champion )	
		if player ["teamId"] == teamid : 
			our_team.append(champion_played)
		else :
			their_team.append(champion_played)


	if 	teamid == 100:
		team1_is_red = True
	else:	
		team1_is_red = False
	#TODO : PREMADE size uitzoeken hoe het werkt.
	premadesize = game["premadeSize"]
	match_id = game["gameId"]
	won = determineWin(game)

	if 	won == 1:
		win = True
	else:	
		win = False
	
	#TODO Iterate over the list to make the match object ! :) 
	try:
		m = match.objects.create(match_id= match_id,team1_is_red=team1_is_red,nr_premade_team1=premadesize,nr_premade_team2=premadesize,won=win,team_1summoner1_id=our_team[0],team_1summoner2_id=our_team[1],team_1summoner3_id=our_team[2],team_1summoner4_id=our_team[3],team_1summoner5_id=our_team[4],team_2summoner1_id=their_team[0],team_2summoner2_id=their_team[1],team_2summoner3_id=their_team[2],team_2summoner4_id=their_team[3],team_2summoner5_id=their_team[4],match_type=type)
	
	except IntegrityError, e:
		logger = logging.getLogger("Double matchid found")
		m = match.objects.filter(match_id = match_id )
	return m

def store_summoner(summoner_id, account_id):
	try:
		summoner = Summoner.objects.get(pk=account_id)
	except Summoner.DoesNotExist:
		summoner = None

	updated = False
	if summoner:
		summoner.delete()
		updated = True
	league_information = getLeagueForPlayerBySummonerID(summoner_id)
	if league_information is None:
		return None
	param_hash = {}
	param_hash["rank"] = ranktoint(league_information["requestorsRank"])
	param_hash["tier"] = tiertoint(league_information["tier"])
	param_hash["name"] = league_information["requestorsName"]
	param_hash["summoner_id"] = summoner_id
	param_hash["account_id"] = account_id	
	leagues = league_information["entries"]["array"]
	summoner_info = filter(lambda x: int(x["playerOrTeamId"]) == summoner_id, leagues)
	summoner_info = summoner_info[0]

	# Todo improve win percentage
	param_hash["hotstreak"] = summoner_info["hotStreak"]
	s1 = Summoner.objects.create( **param_hash )
	print_summoner(s1, updated)
	return s1 

# Store the information for all champions for the given summoner
# return: false if the summoner was recently updated
def store_champions_played(accountId):
	summoner = Summoner.objects.get(pk=accountId)
	if summoner is None:
		return None
	accountstats = getAggregatedStatsByAccountID(accountId)
	param_hash = {}
	for champion_stats in accountstats:
		champion_id = champion_stats["championId"]
		if champion_id not in param_hash:
			param_hash[champion_id] = {}
		try:
			champion_instance = Champion.objects.get(pk=champion_id)
		except:
			continue

		param_hash[champion_id]["champion"] = champion_instance
		param_hash[champion_id]["summoner"] = summoner
		statType 	= champion_stats["statType"]

		if statType == "TOTAL_SESSIONS_PLAYED":
			param_hash[champion_id]["nr_gameswithchamp"] =  champion_stats["value"]
		if statType == "TOTAL_ASSISTS":
			param_hash[champion_id]["average_assists"] =  champion_stats["value"]
		if statType == "TOTAL_DEATHS_PER_SESSION":
			param_hash[champion_id]["average_deaths"] =  champion_stats["value"]
		if statType == "TOTAL_CHAMPION_KILLS":
			param_hash[champion_id]["average_kills"] =  champion_stats["value"]
		if statType == "TOTAL_GOLD_EARNED":
			param_hash[champion_id]["average_gold"] =  champion_stats["value"]

	for champion_id in param_hash:
		params = param_hash[champion_id]
		try:
			champion_instance = Champion.objects.get(pk=champion_id)
		except:
			continue

		try:
			champ_played = ChampionPlayed.objects.get(champion=champion_instance,summoner=summoner)
			champ_played.delete()
		except ChampionPlayed.DoesNotExist:
			pass
		params["average_assists"] = params["average_assists"] // params["nr_gameswithchamp"]
		params["average_deaths"] = params["average_deaths"] // params["nr_gameswithchamp"]
		params["average_kills"] = params["average_kills"] // params["nr_gameswithchamp"]
		params["average_gold"] = params["average_gold"] // params["nr_gameswithchamp"]
		c1 = ChampionPlayed.objects.create(**params)
	print_champion_played(summoner)	

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
	summoner11input = [ matc.team_1summoner1_id.champion_played.nr_gameswithchamp , matc.team_1summoner1_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner1_id.champion_played.champid.key,
	matc.team_1summoner1_id.leaguepoints , tier11 , matc.team_1summoner1_id.rank  , matc.team_1summoner1_id.recentwinpercentage ]
		
	summoner12input = [ matc.team_1summoner2_id.champion_played.nr_gameswithchamp , matc.team_1summoner2_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner2_id.champion_played.champid.key,
	matc.team_1summoner2_id.leaguepoints , tier12 , matc.team_1summoner2_id.rank  , matc.team_1summoner2_id.recentwinpercentage ]

	summoner13input = [ matc.team_1summoner3_id.champion_played.nr_gameswithchamp , matc.team_1summoner3_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner3_id.champion_played.champid.key,
	matc.team_1summoner3_id.leaguepoints , tier13 , matc.team_1summoner3_id.rank  , matc.team_1summoner3_id.recentwinpercentage ]

	summoner14input = [ matc.team_1summoner4_id.champion_played.nr_gameswithchamp , matc.team_1summoner4_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner4_id.champion_played.champid.key,
	matc.team_1summoner4_id.leaguepoints , tier14, matc.team_1summoner3_id.rank  , matc.team_1summoner4_id.recentwinpercentage ]

	summoner15input = [ matc.team_1summoner5_id.champion_played.nr_gameswithchamp , matc.team_1summoner5_id.champion_played.nr_gameswonwithchamp , matc.team_1summoner5_id.champion_played.champid.key,
	matc.team_1summoner5_id.leaguepoints , tier15 , matc.team_1summoner5_id.rank  , matc.team_1summoner5_id.recentwinpercentage ]

	summoner21input = [ matc.team_2summoner1_id.champion_played.nr_gameswithchamp , matc.team_2summoner1_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner1_id.champion_played.champid.key,
	matc.team_2summoner1_id.leaguepoints , tier21 , matc.team_2summoner1_id.rank  , matc.team_2summoner1_id.recentwinpercentage ]
		
	summoner22input = [ matc.team_2summoner2_id.champion_played.nr_gameswithchamp , matc.team_2summoner2_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner2_id.champion_played.champid.key,
	matc.team_2summoner2_id.leaguepoints , tier22 , matc.team_2summoner2_id.rank  , matc.team_2summoner2_id.recentwinpercentage ]

	summoner23input = [ matc.team_2summoner3_id.champion_played.nr_gameswithchamp , matc.team_2summoner3_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner3_id.champion_played.champid.key,
	matc.team_2summoner3_id.leaguepoints , tier23 , matc.team_2summoner3_id.rank  , matc.team_2summoner3_id.recentwinpercentage ]

	summoner24input = [ matc.team_2summoner4_id.champion_played.nr_gameswithchamp , matc.team_2summoner4_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner4_id.champion_played.champid.key,
	matc.team_2summoner4_id.leaguepoints , tier24, matc.team_2summoner3_id.rank  , matc.team_2summoner4_id.recentwinpercentage ]

	summoner25input = [ matc.team_2summoner5_id.champion_played.nr_gameswithchamp , matc.team_2summoner5_id.champion_played.nr_gameswonwithchamp , matc.team_2summoner5_id.champion_played.champid.key,
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

def print_summoner(summoner, updated):
	if updated:
		print "Summoner %s updated(accountId=%s, summonerId=%s) " % (summoner.name, summoner.account_id, summoner.summoner_id)
	else:
		print "Summoner %s added(accountId=%s, summonerId=%s) " % (summoner.name, summoner.account_id, summoner.summoner_id)
def print_champion_played(summoner):
	print "champions for summoner %s updated(accountId=%s, summonerId=%s) " % (summoner.name, summoner.account_id, summoner.summoner_id)

def print_match(match):
	print match