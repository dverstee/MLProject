#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from  lolpredictor.predictor.models import *
from datetime import *
from api import *
from django.db import IntegrityError
from preprocessing import *
import globals
logger = logging.getLogger(__name__)

REFRESH_SUMMONER_INTERVAL = 3600*24 # One day refresh interval
REFRESH_SUMMONER_CHALMPS_INTERVAL =3600*4


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
	recentadds=globals.nrgamesadded
	recenterrors =globals.nrerrors
	for game in games:
		if game["queueType"] == "RANKED_SOLO_5x5" :
			print "Storing Ranked game" 
			m = store_match(game,"RANKED_SOLO_5x5",accountid)
			if m is not None :
				globals.nrgamesadded += 1
			else :
				globals.nrerrors += 1

	if recentadds-globals.nrgamesadded == 0  and recenterrors-globals.nrerrors==0  :
		logger.debug("Not enough matches")
		print "Not enough matches"		
		return None

	return globals.nrgamesadded 

	
def store_match(game, type, account_id):
	print game
	our_team = []
	their_team = []
	championid = game["championId"]
	summoner_id = getSummonerIdByAccountId(account_id)
	if summoner_id is None:
		return None

	team_id = game["teamId"]
	match_id = game["gameId"]
	if Match.objects.filter(match_id=match_id).count() > 0:
		return None
	
	try:
		m = Match.objects.get(match_id=match_id)
		print "This match was already stored"
		globals.nrofupdates += 1
		return m
	except Match.DoesNotExist, e:
		pass
	
	summoner = store_summoner(summoner_id, account_id)	
	champion = Champion.objects.get(pk=championid)
	if champion is None or summoner is None:
		return None
	try:
		store_champions_played(account_id, champion)
	except KeyError, e:
		print "Error storing champions"
		return None	

	try:
		champPlayed=ChampionPlayed.objects.get(summoner = summoner, champion=champion)	
	except ChampionPlayed.DoesNotExist:		
		print "Exception DoesNotExist"		
		return None	
		
	our_team.append(champPlayed)
	#Store Others
	fellowplayers = game["fellowPlayers"]["array"]
	for player in fellowplayers:	
		champion_id = player["championId"]	
		summoner_id = player["summonerId"]	

			
		summoner = store_summoner(summoner_id, None)		
		if summoner == None:
			return None
		champion = Champion.objects.get(pk=champion_id)	
		try:
			store_champions_played(summoner.account_id, champion)
		except KeyError, e:
			print "Error storing champions"
			return None

		
		try:
			champion_played = ChampionPlayed.objects.get(summoner = summoner, champion=champion )	
		except ChampionPlayed.DoesNotExist:			
			print "Exception DoesNotExist"
			print summoner
			print champion

		if player ["teamId"] == team_id : 
			our_team.append(champion_played)
		else :
			their_team.append(champion_played)

	if 	team_id == 100:
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
	try:
		m = Match.objects.create(match_id= match_id,team1_is_red=team1_is_red,nr_premade_team1=premadesize,nr_premade_team2=premadesize,won=win,team_1summoner1_id=our_team[0],team_1summoner2_id=our_team[1],team_1summoner3_id=our_team[2],team_1summoner4_id=our_team[3],team_1summoner5_id=our_team[4],team_2summoner1_id=their_team[0],team_2summoner2_id=their_team[1],team_2summoner3_id=their_team[2],team_2summoner4_id=their_team[3],team_2summoner5_id=their_team[4],match_type=type)
		sort_match_champions(m.match_id)
		print_match(m)
	except IntegrityError as e:
		logger = logging.getLogger("Double matchid found")
		return None
	return m


def store_summoner(summoner_id,account_id):	
	try:
		summoner = Summoner.objects.get(summoner_id=summoner_id)
		diff = datetime.now() - summoner.updated_at.replace(tzinfo=None) - timedelta(seconds=REFRESH_SUMMONER_INTERVAL)
		if diff.days < 0:			
			print_summoner(summoner,True,False)
			return summoner
	except Summoner.DoesNotExist:
		summoner = None
	updated = False
	if summoner:
		summoner.delete()
		updated = True

	if account_id is None:
		account_id = getAccountIdBySummonerId(summoner_id)
	if account_id is None:
		return None	
	param_hash = {}	
	try : 
		league_information = getLeagueForPlayerBySummonerID(summoner_id)
		param_hash["rank"] = ranktoint(league_information["requestorsRank"])
		param_hash["tier"] = tiertoint(league_information["tier"])
		param_hash["name"] = league_information["requestorsName"]
		if league_information is None:
			print summoner_id
			print "League is none"
			return None
		
	except ValueError:		
		param_hash["rank"] = 4
		param_hash["tier"] = 2
		param_hash["name"] = getNameByAccountId(account_id)

	param_hash["summoner_id"] = summoner_id
	param_hash["account_id"] = account_id	
	param_hash["updated_at"] = datetime.now()
	leagues = league_information["entries"]["array"]
	summoner_info = filter(lambda x: int(x["playerOrTeamId"]) == summoner_id, leagues)
	summoner_info = summoner_info[0]

	# Todo improve win percentage
	param_hash["hotstreak"] = summoner_info["hotStreak"]
	s1 = Summoner.objects.create( **param_hash )

	print_summoner(s1, updated,True)
	return s1 


# Store the information for all champions for the given summoner
# return: false if the summoner was recently updated
def store_champions_played(accountId, champion):
	summoner = Summoner.objects.get(pk=accountId)

	try:
		cp = ChampionPlayed.objects.get(summoner=summoner,champion=champion)
		if cp is not None:
			diff =datetime.now() - cp.champions_updated_at.replace(tzinfo=None) - timedelta(seconds=REFRESH_SUMMONER_INTERVAL)
			if diff.days < 0:
				print_champion_played(summoner,False)
				return False
	except:		
		pass

	accountstats = getAggregatedStatsByAccountID(accountId)
	if	accountstats is None :
		print "Can't get accountstats"
		raise KeyError
	param_hash = {}
	for champion_stats in accountstats:
		champion_id = champion_stats["championId"]
		# Only store the relevant
		if champion_id != champion.key:
			continue
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
		params["average_assists"] = params["average_assists"] / params["nr_gameswithchamp"]
		params["average_deaths"] = params["average_deaths"] / params["nr_gameswithchamp"]
		params["average_kills"] = params["average_kills"] / params["nr_gameswithchamp"]
		params["average_gold"] = params["average_gold"] / params["nr_gameswithchamp"]
		c1 = ChampionPlayed.objects.create(**params)
	print_champion_played(summoner,True)	
	return True

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

def getMinimalDatafromMatch(matc,preprocessing):
	input = [matchups_to_win_rate(matc)]
	if matc.team1_is_red:
		input += champion_played_to_features(matc.team_1summoner1_id)
		input += champion_played_to_features(matc.team_1summoner2_id)
		input += champion_played_to_features(matc.team_1summoner3_id)
		input += champion_played_to_features(matc.team_1summoner4_id)
		input += champion_played_to_features(matc.team_1summoner5_id)

	input += champion_played_to_features(matc.team_1summoner1_id)
	input += champion_played_to_features(matc.team_1summoner2_id)
	input += champion_played_to_features(matc.team_1summoner3_id)
	input += champion_played_to_features(matc.team_1summoner4_id)
	input += champion_played_to_features(matc.team_1summoner5_id)

	if not matc.team1_is_red:
		input += champion_played_to_features(matc.team_1summoner1_id)
		input += champion_played_to_features(matc.team_1summoner2_id)
		input += champion_played_to_features(matc.team_1summoner3_id)
		input += champion_played_to_features(matc.team_1summoner4_id)
		input += champion_played_to_features(matc.team_1summoner5_id)
	print input
	return input


def champion_played_to_features(champion_played):
	# 0 to 1 ranking
	ranking = float((champion_played.summoner.tier) - 1)/5.0 + float(4 - (champion_played.summoner.rank-1))/50.0
	if champion_played.average_deaths:
		kdr		= float(champion_played.average_kills + champion_played.average_assists/2) / float(champion_played.average_deaths)
	else:
		kdr     = float(champion_played.average_kills + champion_played.average_assists/2) * 1.5
	normalized_gold = float(champion_played.average_gold) / float(globals.goldnormalization)
	return [ranking, kdr, normalized_gold]

def matchups_to_win_rate(match):
	if matc.team1_is_red:
		team_1 = [match.team_1summoner1_id, match.team_1summoner2_id, match.team_1summoner3_id, match.team_1summoner4_id, match.team_1summoner5_id]
		team_2 = [match.team_2summoner1_id, match.team_2summoner2_id, match.team_2summoner3_id, match.team_2summoner4_id, match.team_2summoner5_id]
	else:
		team_1 = [match.team_2summoner1_id, match.team_2summoner2_id, match.team_2summoner3_id, match.team_2summoner4_id, match.team_2summoner5_id]
		team_2 = [match.team_1summoner1_id, match.team_1summoner2_id, match.team_1summoner3_id, match.team_1summoner4_id, match.team_1summoner5_id]
	
	win_rates = []
	for i in range(len(team_1)):
		try:
			matchup = Matchup.objects.get(champion_1=team_1[i].champion, champion_2=team_2[i].champion)
			win_rates.append(matchup.win_rate)
		except:
			pass
	synergys = []
	try:
		synergys.append(Synergy.objects.get(champion_1=team_1[3].champion, champion_2=team_1[4].champion).win_rate)
	except:
		pass
	try:
		synergys.append(1 - Synergy.objects.get(champion_1=team_2[3].champion, champion_2=team_2[4].champion).win_rate)
	except:
		pass
	if synergys:
		win_rates.append(sum(synergys)/len(synergys))
	if win_rates:
		return sum(win_rates)/len(win_rates)
	else:
		return 0.5


def getBasicDatafromMatch(matc,preprocessing):
	input=[]
	goldnormalization =10000.0

	if preprocessing==True  :		
		return preprocessdata(matc)
				

	matchinput =  [ int(matc.team1_is_red) ] 	

	summoner11input = [ matc.team_1summoner1_id.summoner.tier ,  matc.team_1summoner1_id.summoner.rank ]
	championplayed11input = [matc.team_1summoner1_id.nr_gameswithchamp ,matc.team_1summoner1_id.average_kills,
	matc.team_1summoner1_id.average_deaths, matc.team_1summoner1_id.average_assists,float(matc.team_1summoner1_id.average_gold)/float(goldnormalization)]

		
	summoner12input = [ matc.team_1summoner2_id.summoner.tier ,  matc.team_1summoner2_id.summoner.rank, 
	int(matc.team_1summoner2_id.summoner.hotstreak) ]
	championplayed12input = [matc.team_1summoner2_id.nr_gameswithchamp ,matc.team_1summoner2_id.average_kills,
	matc.team_1summoner2_id.average_deaths, matc.team_1summoner2_id.average_assists,float(matc.team_1summoner2_id.average_gold)/float(goldnormalization)]

	summoner13input = [ matc.team_1summoner3_id.summoner.tier ,  matc.team_1summoner3_id.summoner.rank, 
	int(matc.team_1summoner3_id.summoner.hotstreak) ]
	championplayed13input = [matc.team_1summoner3_id.nr_gameswithchamp ,matc.team_1summoner3_id.average_kills,
	matc.team_1summoner3_id.average_deaths, matc.team_1summoner3_id.average_assists,float(matc.team_1summoner3_id.average_gold)/float(goldnormalization)]

	summoner14input = [ matc.team_1summoner4_id.summoner.tier ,  matc.team_1summoner4_id.summoner.rank, 
	int(matc.team_1summoner4_id.summoner.hotstreak) ]
	championplayed14input = [matc.team_1summoner4_id.nr_gameswithchamp ,matc.team_1summoner4_id.average_kills,
	matc.team_1summoner4_id.average_deaths, matc.team_1summoner4_id.average_assists,float(matc.team_1summoner4_id.average_gold)/float(goldnormalization)]

	summoner15input = [ matc.team_1summoner5_id.summoner.tier ,  matc.team_1summoner5_id.summoner.rank, 
	int(matc.team_1summoner5_id.summoner.hotstreak) ]
	championplayed15input = [matc.team_1summoner5_id.nr_gameswithchamp ,matc.team_1summoner5_id.average_kills,
	matc.team_1summoner5_id.average_deaths, matc.team_1summoner5_id.average_assists,float(matc.team_1summoner5_id.average_gold)/float(goldnormalization)]

	summoner21input = [ matc.team_2summoner1_id.summoner.tier ,  matc.team_2summoner1_id.summoner.rank, 
	int(matc.team_2summoner1_id.summoner.hotstreak) ]
	championplayed21input = [matc.team_2summoner1_id.nr_gameswithchamp ,matc.team_2summoner1_id.average_kills,
	matc.team_2summoner1_id.average_deaths, matc.team_2summoner1_id.average_assists,float(matc.team_2summoner1_id.average_gold)/float(goldnormalization)]

	summoner22input = [ matc.team_2summoner2_id.summoner.tier ,  matc.team_2summoner2_id.summoner.rank, 
	int(matc.team_2summoner2_id.summoner.hotstreak )]
	championplayed22input = [matc.team_2summoner2_id.nr_gameswithchamp ,matc.team_2summoner2_id.average_kills,
	matc.team_2summoner2_id.average_deaths, matc.team_2summoner2_id.average_assists,float(matc.team_2summoner2_id.average_gold)/float(goldnormalization)]

	summoner23input = [ matc.team_2summoner3_id.summoner.tier ,  matc.team_2summoner3_id.summoner.rank, 
	int(matc.team_2summoner3_id.summoner.hotstreak )]
	championplayed23input = [matc.team_2summoner3_id.nr_gameswithchamp ,matc.team_2summoner3_id.average_kills,
	matc.team_2summoner3_id.average_deaths, matc.team_2summoner3_id.average_assists,float(matc.team_2summoner3_id.average_gold)/float(goldnormalization)]

	summoner24input = [ matc.team_2summoner4_id.summoner.tier ,  matc.team_2summoner4_id.summoner.rank, 
	int(matc.team_2summoner4_id.summoner.hotstreak )]
	championplayed24input = [matc.team_2summoner4_id.nr_gameswithchamp ,matc.team_2summoner4_id.average_kills,
	matc.team_2summoner4_id.average_deaths, matc.team_2summoner4_id.average_assists,float(matc.team_2summoner4_id.average_gold)/float(goldnormalization)]

	summoner25input = [ matc.team_2summoner5_id.summoner.tier ,  matc.team_2summoner5_id.summoner.rank, 
	int(matc.team_2summoner5_id.summoner.hotstreak) ]
	championplayed25input = [matc.team_2summoner5_id.nr_gameswithchamp ,matc.team_2summoner5_id.average_kills,
	matc.team_2summoner5_id.average_deaths, matc.team_2summoner5_id.average_assists,float(matc.team_2summoner5_id.average_gold)/float(goldnormalization)]

	input.extend(matchinput)
	input.extend(summoner11input)
	input.extend(championplayed11input)
	input.extend(summoner12input)
	input.extend(championplayed12input)
	input.extend(summoner13input)
	input.extend(championplayed13input)
	input.extend(summoner14input)
	input.extend(championplayed14input)
	input.extend(summoner15input)
	input.extend(championplayed15input)
	input.extend(summoner21input)
	input.extend(championplayed21input)
	input.extend(summoner22input)
	input.extend(championplayed22input)
	input.extend(summoner23input)
	input.extend(championplayed23input)
	input.extend(summoner24input)
	input.extend(championplayed24input)
	input.extend(summoner25input)
	input.extend(championplayed25input)
	input.extend(get_win_rates(matc))
	return input


def preprocessdata(matc):
	tiers=[]
	tiers.append(matc.team_1summoner1_id.summoner.tier)
	tiers.append(matc.team_1summoner2_id.summoner.tier)
	tiers.append(matc.team_1summoner3_id.summoner.tier)
	tiers.append(matc.team_1summoner4_id.summoner.tier)
	tiers.append(matc.team_1summoner5_id.summoner.tier)
	tiers2=[]
	tiers2.append(matc.team_2summoner1_id.summoner.tier)
	tiers2.append(matc.team_2summoner2_id.summoner.tier)
	tiers2.append(matc.team_2summoner3_id.summoner.tier)
	tiers2.append(matc.team_2summoner4_id.summoner.tier)
	tiers2.append(matc.team_2summoner5_id.summoner.tier)
	ranks=[]
	ranks.append(matc.team_1summoner1_id.summoner.rank)	
	ranks.append(matc.team_1summoner2_id.summoner.rank)	
	ranks.append(matc.team_1summoner3_id.summoner.rank)	
	ranks.append(matc.team_1summoner4_id.summoner.rank)	
	ranks.append(matc.team_1summoner5_id.summoner.rank)	
	ranks2=[]
	ranks2.append(matc.team_2summoner1_id.summoner.rank)	
	ranks2.append(matc.team_2summoner2_id.summoner.rank)	
	ranks2.append(matc.team_2summoner3_id.summoner.rank)	
	ranks2.append(matc.team_2summoner4_id.summoner.rank)	
	ranks2.append(matc.team_2summoner5_id.summoner.rank)	

	our_tiers = [0, 0, 0 , 0 , 0 ]
	their_tiers = [0, 0, 0 , 0 , 0]
	our_ranks= [0, 0, 0 , 0 , 0]
	their_ranks= [0, 0, 0 , 0 , 0]
	our_hotsreaks=int(matc.team_1summoner1_id.summoner.hotstreak)
	+int(matc.team_1summoner2_id.summoner.hotstreak )
	+int(matc.team_1summoner3_id.summoner.hotstreak )
	+int(matc.team_1summoner4_id.summoner.hotstreak )
	+int(matc.team_1summoner5_id.summoner.hotstreak )

	their_hotsreaks=int(matc.team_1summoner1_id.summoner.hotstreak)
	+int(matc.team_2summoner2_id.summoner.hotstreak )
	+int(matc.team_2summoner3_id.summoner.hotstreak )
	+int(matc.team_2summoner4_id.summoner.hotstreak )
	+int(matc.team_2summoner5_id.summoner.hotstreak)


	our_kills=matc.team_1summoner1_id.average_kills
	+matc.team_1summoner2_id.average_kills 
	+matc.team_1summoner3_id.average_kills 
	+matc.team_1summoner4_id.average_kills 
	+matc.team_1summoner5_id.average_kills 

	their_kills=matc.team_1summoner1_id.average_kills
	+matc.team_2summoner2_id.average_kills 
	+matc.team_2summoner3_id.average_kills 
	+matc.team_2summoner4_id.average_kills 
	+matc.team_2summoner5_id.average_kills 

	our_games=matc.team_1summoner1_id.nr_gameswithchamp
	+matc.team_1summoner2_id.nr_gameswithchamp 
	+matc.team_1summoner3_id.nr_gameswithchamp 
	+matc.team_1summoner4_id.nr_gameswithchamp 
	+matc.team_1summoner5_id.nr_gameswithchamp 

	their_games=matc.team_1summoner1_id.nr_gameswithchamp
	+matc.team_2summoner2_id.nr_gameswithchamp 
	+matc.team_2summoner3_id.nr_gameswithchamp 
	+matc.team_2summoner4_id.nr_gameswithchamp 
	+matc.team_2summoner5_id.nr_gameswithchamp 

	our_assists=matc.team_1summoner1_id.average_assists
	+matc.team_1summoner2_id.average_assists 
	+matc.team_1summoner3_id.average_assists 
	+matc.team_1summoner4_id.average_assists 
	+matc.team_1summoner5_id.average_assists 

	their_assists=matc.team_1summoner1_id.average_assists
	+matc.team_2summoner2_id.average_assists 
	+matc.team_2summoner3_id.average_assists 
	+matc.team_2summoner4_id.average_assists 
	+matc.team_2summoner5_id.average_assists 

	our_deaths=matc.team_1summoner1_id.average_deaths
	+matc.team_1summoner2_id.average_deaths 
	+matc.team_1summoner3_id.average_deaths 
	+matc.team_1summoner4_id.average_deaths 
	+matc.team_1summoner5_id.average_deaths 

	their_deaths=matc.team_1summoner1_id.average_deaths
	+matc.team_2summoner2_id.average_deaths 
	+matc.team_2summoner3_id.average_deaths 
	+matc.team_2summoner4_id.average_deaths 
	+matc.team_2summoner5_id.average_deaths 

	our_gold=matc.team_1summoner1_id.average_gold
	+matc.team_1summoner2_id.average_gold 
	+matc.team_1summoner3_id.average_gold 
	+matc.team_1summoner4_id.average_gold 
	+matc.team_1summoner5_id.average_gold 

	their_gold=matc.team_1summoner1_id.average_gold
	+matc.team_2summoner2_id.average_gold 
	+matc.team_2summoner3_id.average_gold 
	+matc.team_2summoner4_id.average_gold 
	+matc.team_2summoner5_id.average_gold 

	for t in tiers:		
		our_tiers[t-1]=our_tiers[t-1]+1
	for t in tiers2:		
		their_tiers[t-1]=their_tiers[t-1]+1
	for t in ranks:		
		our_ranks[t-1]=our_ranks[t-1]+1
	for t in ranks2:	
		their_ranks[t-1]=their_ranks[t-1]+1	

	matchinput =  [ matc.team1_is_red ]	

	input=[]
	input.extend(matchinput)
	input.extend(our_tiers)
	input.extend(their_tiers)
	input.extend(our_ranks)
	input.extend(their_ranks)
	input.append(our_hotsreaks)
	input.append(their_hotsreaks)
	input.append(our_kills)
	input.append(their_kills)
	input.append(our_games)
	input.append(their_games)
	input.append(our_assists)
	input.append(their_assists)
	input.append(our_deaths)
	input.append(their_deaths)
	input.append(our_gold)
	input.append(their_gold)
	return input


def print_summoner(summoner, updated, realupdate):
	try:
		if updated:
			if realupdate : 
				print "Summoner %s updated(accountId=%s, summonerId=%s) " % (summoner.name, summoner.account_id, summoner.summoner_id)
			else :
				print "No update was required for Summoner %s (accountId=%s, summonerId=%s) " % (summoner.name, summoner.account_id, summoner.summoner_id)
		else:
			print "Summoner %s added(accountId=%s, summonerId=%s) " % (summoner.name, summoner.account_id, summoner.summoner_id)
	except:
		pass


def print_champion_played(summoner,updated):
	try:
		if updated:
			print "champions for summoner %s updated(accountId=%s, summonerId=%s) " % (summoner.name, summoner.account_id, summoner.summoner_id)
		else:
			print "No need to update champions for summoner %s (accountId=%s, summonerId=%s) " % (summoner.name, summoner.account_id, summoner.summoner_id)
	except Exception:
		return None

def print_match(match):
	print match