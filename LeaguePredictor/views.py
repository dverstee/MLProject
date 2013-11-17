from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
from LeaguePredictor.models import Summoner
from pprint import pprint
import unirest
import logging
import sys
logger = logging.getLogger(__name__)
def index(request):
 

	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUW/summoner/getAllPublicSummonerDataByAccount/26967519",
	  
	headers={
	    "X-Mashape-Authorization": "XsKOUv6r8adM9zHxkDC0sBXQvHEhs2vV"
	  	}
	);
	values = json.loads(response.raw_body)	
	print values
	name = values['summoner']['internalName']

 	

	return HttpResponse(name)



