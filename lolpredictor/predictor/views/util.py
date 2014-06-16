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
def parse_ranked_games(games,id):

	recentadds=globals.nrgamesadded
	recenterrors =globals.nrerrors
	for game in games:
		if game["subType"] == "RANKED_SOLO_5x5" :			
			m = store_match(game,"RANKED_SOLO_5x5",id,"euw")
			if m is not None :
				globals.nrgamesadded += 1
			else :
				globals.nrerrors += 1

	if recentadds-globals.nrgamesadded == 0  and recenterrors-globals.nrerrors==0  :
		logger.debug("Not enough matches")
		print "Not enough matches"		
		return None

	return globals.nrgamesadded 	
def store_match(game, type,id,region):


	our_summonersids = [] 
	their_summonersids=[]
	all_ids=[]
	our_team = []
	their_team = []
	championid = game["championId"]
	team_id = game["teamId"]
	match_id = game["gameId"]

	


	try:
		m = Match.objects.get(match_id=match_id)
		print "This match was already stored"
		globals.nrofupdates += 1
		return m
	except Match.DoesNotExist, e:
		pass
	
	our_summonersids.append(id)
	fellowplayers = game["fellowPlayers"]
	for player in fellowplayers:
		if player["teamId"] == team_id : 
			our_summonersids.append(player["summonerId"])
		else :
			their_summonersids.append(player["summonerId"])	
	all_ids=our_summonersids + their_summonersids
	store_summoners(all_ids,region)
	print("stored summoners")
		
	champion = Champion.objects.get(pk=championid)	
	store_champions_played(id, champion)
	
	try:
		summoner = Summoner.objects.get(account_id=id)
		champPlayed=ChampionPlayed.objects.get(summoner = summoner, champion=champion)	
	except ChampionPlayed.DoesNotExist:	
		print "Exception DoesNotExist 1"
		return None
		
		
	our_team.append(champPlayed)
	#Store Others
	fellowplayers = game["fellowPlayers"]
	for player in fellowplayers:	
		champion_id = player["championId"]	
		summoner_id = player["summonerId"]
		try:
			champion = Champion.objects.get(pk=champion_id)
		except Champion.DoesNotExist:
			print champion_id
		try:
			store_champions_played(summoner_id, champion)
		except KeyError, e:
			print "Error storing champions"
			return None		
		try:
			summoner = Summoner.objects.get(account_id=summoner_id)
			champion_played = ChampionPlayed.objects.get(summoner = summoner, champion=champion )	
		except ChampionPlayed.DoesNotExist:			
			print "Exception DoesNotExist 2"
			return None		

		if player["teamId"] == team_id : 
			our_team.append(champion_played)
		else :
			their_team.append(champion_played)

	if team_id == 100:
		team1_is_red = True
	else:	
		team1_is_red = False
	#TODO : PREMADE size uitzoeken hoe het werkt.	
	won = determineWin(game)	
	premadesize=0	
	print("all summoners and champions played stored")
	#TODO Iterate over the list to make the match object ! :) 
	try:
		m = Match.objects.create(match_id= match_id,team1_is_red=team1_is_red,nr_premade_team1=premadesize,nr_premade_team2=premadesize,won=won,team_1summoner1_id=our_team[0],team_1summoner2_id=our_team[1],team_1summoner3_id=our_team[2],team_1summoner4_id=our_team[3],team_1summoner5_id=our_team[4],team_2summoner1_id=their_team[0],team_2summoner2_id=their_team[1],team_2summoner3_id=their_team[2],team_2summoner4_id=their_team[3],team_2summoner5_id=their_team[4],match_type=type)
		sort_match_champions(m.match_id)
		print_match(m)
	except IntegrityError as e:
		logger = logging.getLogger("Double matchid found")
		return None
	return m

def store_summoners(ids,region):
	#check which ids are alread stored.	
	badid=[]
	for sid in ids:			
		try:
			summoners = Summoner.objects.filter(account_id=sid)
			if len(summoners)>1:
				print("more than one summoner with this id.")
				summoners.delete()				
			summoner = Summoner.objects.get(account_id=sid)			
			diff = datetime.now() - summoner.updated_at.replace(tzinfo=None) - timedelta(seconds=REFRESH_SUMMONER_INTERVAL)
			if diff.days < 0:	
				badid.append(sid)					
				print_summoner(summoner,True,False)				
		except Summoner.DoesNotExist:
			pass
		updated = False		
	for id in badid:		
		ids.remove(id)	
		if len(ids)==0:
			print("ALL SUMMONERS ALREADY STORED")
			return True
	#for the remaining ids make a call.
	param_hash = {}	

	
			
	leagues = getLeagueForPlayerById(str(','.join(str(v) for v in ids)))		
	for id in ids:	
		try :  			
			league_information=leagues[str(id)]			
			if league_information == 503 :
				return 503

			for league in league_information:			       
				if league["queue"] == "RANKED_SOLO_5x5": 				
					entries = league["entries"]
					param_hash["tier"] = tiertoint(league["tier"])
					for entry in entries:
						param_hash["rank"] = ranktoint(entry["division"])
						param_hash["name"] = entry["playerOrTeamName"]
						param_hash["hotstreak"] = entry["isHotStreak"]
			param_hash["region"] = 	region
			param_hash["account_id"] = id	
			param_hash["updated_at"] = datetime.now()
			param_hash["sid"]=Summoner.objects.count()+1
			s1 = Summoner.objects.create( **param_hash )
			print_summoner(s1,updated,True)
		except:		
			print("Summoner unranked.")
			summ = getSummonerById(id)
			param_hash["tier"] = 0
			param_hash["rank"] = 0
			param_hash["name"] = summ[str(id)]["name"]
			param_hash["hotstreak"] = False
			param_hash["region"] = 	region
			param_hash["account_id"] = id	
			param_hash["updated_at"] = datetime.now()
			param_hash["sid"]=Summoner.objects.count()+1
			s1 = Summoner.objects.create( **param_hash )
			print_summoner(s1,updated,True)			
	return True
	

# Store the information for all champions for the given summoner
# return: false if the summoner was recently updated
def store_champions_played(id, champion):
	summoner = Summoner.objects.get(account_id=id)	
	try:
		cp = ChampionPlayed.objects.get(summoner=summoner,champion=champion)
		if cp is not None:
			diff =datetime.now() - cp.champions_updated_at.replace(tzinfo=None) - timedelta(seconds=REFRESH_SUMMONER_INTERVAL)
			if diff.days < 0:
				print_champion_played(summoner,False)
				return False
	except:		
		pass
	
	accountstats = getAggregatedStatsById(id)
	accountstats = 	accountstats["champions"]
	"""TODO : rework
	 if	accountstats is None :
		print "Can't get accountstats"
		raise KeyError"""
	param_hash = {}
	for champion_stats in accountstats:
		champion_id = champion_stats["id"]		
		#review	
		if champion_id not in param_hash:
			param_hash[champion_id] = {}
		try:
			champion_instance = Champion.objects.get(pk=champion_id)
		except:
			continue
			
		param_hash[champion_id]["champion"] = champion_instance
		param_hash[champion_id]["summoner"] = summoner		
		stats = champion_stats["stats"]		
		
		param_hash[champion_id]["nr_gameswithchamp"] = stats["totalSessionsPlayed"]
		param_hash[champion_id]["average_assists"] = stats["totalAssists"]
		param_hash[champion_id]["average_deaths"] = stats["totalDeathsPerSession"]
		param_hash[champion_id]["average_kills"] = stats["totalChampionKills"]
		param_hash[champion_id]["average_gold"] = stats["totalGoldEarned"]
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
	return game["stats"]["win"]
	
def getMinimalDatafromMatch(matc, preprocessing, reverse):
	input = matchups_to_win_rate(matc, reverse)

	if not reverse:
		input += champion_played_to_features(matc.team_1summoner1_id)
		input += champion_played_to_features(matc.team_1summoner2_id)
		input += champion_played_to_features(matc.team_1summoner3_id)
		input += champion_played_to_features(matc.team_1summoner4_id)
		input += champion_played_to_features(matc.team_1summoner5_id)

		input += champion_played_to_features(matc.team_2summoner1_id)
		input += champion_played_to_features(matc.team_2summoner2_id)
		input += champion_played_to_features(matc.team_2summoner3_id)
		input += champion_played_to_features(matc.team_2summoner4_id)
		input += champion_played_to_features(matc.team_2summoner5_id)
	else:
		input += champion_played_to_features(matc.team_2summoner1_id)
		input += champion_played_to_features(matc.team_2summoner2_id)
		input += champion_played_to_features(matc.team_2summoner3_id)
		input += champion_played_to_features(matc.team_2summoner4_id)
		input += champion_played_to_features(matc.team_2summoner5_id)

		input += champion_played_to_features(matc.team_1summoner1_id)
		input += champion_played_to_features(matc.team_1summoner2_id)
		input += champion_played_to_features(matc.team_1summoner3_id)
		input += champion_played_to_features(matc.team_1summoner4_id)
		input += champion_played_to_features(matc.team_1summoner5_id)


	if (matc.team1_is_red and not reverse) or (not matc.team1_is_red and reverse):
		input += [1, 0]
	else:
		input += [0, 1]
	
	return input
def champion_played_to_features(champion_played):
	#print "%s : %d/%d/%d" % (champion_played.champion, champion_played.average_kills, champion_played.average_deaths, champion_played.average_assists)
	# 0 to 1 ranking
	ranking = float((champion_played.summoner.tier) - 1)/5.0 + float(4 - (champion_played.summoner.rank-1))/50.0
	if champion_played.average_deaths:
		kdr		= float(champion_played.average_kills + champion_played.average_assists/2) / float(champion_played.average_deaths)
	else:
		kdr     = float(champion_played.average_kills + champion_played.average_assists/2) * 1.5
	normalized_gold = float(champion_played.average_gold) / float(globals.goldnormalization)
	return [ranking, kdr, normalized_gold]
def matchups_to_win_rate(match, reverse):
	if not reverse:
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
def getBasicDatafromMatch(matc,preprocessing, reverse):
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
				print "Summoner %s updated(accountId=%s) " % (summoner.name, summoner.account_id)
			else :
				print "No update was required for Summoner %s (accountId=%s) " % (summoner.name, summoner.account_id)
		else:
			print "Summoner %s added(accountId=%s) " % (summoner.name, summoner.account_id)
	except:
		pass
def print_champion_played(summoner,updated):
	try:
		if updated:
			print "champions for summoner %s updated(accountId=%s) " % (summoner.name, summoner.account_id)
		else:
			print "No need to update champions for summoner %s (accountId=%s) " % (summoner.name, summoner.account_id)
	except Exception:
		return None
def print_match(match):
	print match