from django.shortcuts import render
import json
import unirest
import logging

logger = logging.getLogger(__name__)


def index(request):
 	if request.method == 'GET':
		return render(request, 'LeaguePredictor/index.html')
	if request.method == 'POST':
		name = request.POST["SummonerName"]
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
			return render(request, 'LeaguePredictor/info.html', my_hash)
		else:
			return render(request, 'LeaguePredictor/index.html')

def parseChampionlist(champions):
	parsed_list = []
	for key, champion in champions.items():
		champion_hash = {}
		champion_hash["id"] = champion["championId"]
		champion_hash["games"] = champion["totalGamesPlayed"]
		champion_hash["image"] = "https://github.com/rwarasaurus/league-of-legends-database/blob/master/icons/%d.jpg?raw=true" % champion["championId"]
		parsed_list.append(champion_hash)
	return parsed_list
def getAccountIdByName(name):
	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getSummonerByName/%s" % name,
	headers={
    	"X-Mashape-Authorization": "aa3OmkDWY3pvnQxfLQJnWa6KGdUHOPHl"
  	});
  	values = json.loads(response.raw_body)	
  	if 'acctId' in values:
  		return values['acctId']
  	return None

def getInfoBySummonerId(accountId):
   	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getAllPublicSummonerDataByAccount/%s" % accountId,
	headers={
		"X-Mashape-Authorization": "aa3OmkDWY3pvnQxfLQJnWa6KGdUHOPHl"
		});
	values = json.loads(response.raw_body)	
	if values:
		return values
	return None

def getTopPlayedChampionsBySummonerId(accountId):
	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/retrieveTopPlayedChampions/%s" % accountId,
	headers={
		"X-Mashape-Authorization": "aa3OmkDWY3pvnQxfLQJnWa6KGdUHOPHl"
		});
	values = json.loads(response.raw_body)	
	if values:
		return values
	return None