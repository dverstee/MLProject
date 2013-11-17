from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.template import Context
import json
from LeaguePredictor.models import Summoner
from pprint import pprint
import unirest
import logging
import sys
logger = logging.getLogger(__name__)


def index(request):
	print request
 	if request.method == 'GET':

		return render(request, 'LeaguePredictor/index.html')


	if request.method == 'POST':


		response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/NA/summoner/getAllPublicSummonerDataByAccount/196272",
	  
		headers={
	    "X-Mashape-Authorization": "aa3OmkDWY3pvnQxfLQJnWa6KGdUHOPHl"
	  	}
		);
		values = json.loads(response.raw_body)		
		name = values['summoner']['internalName']	
		return HttpResponse(name)


	
 	
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
	


def getInfoBySummonerName():
   print "aa"