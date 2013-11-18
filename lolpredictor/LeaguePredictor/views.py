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
	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUNE/summoner/getSummonerByName/%s" % name,
	headers={
    	"X-Mashape-Authorization": "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"
  	});
  	values = json.loads(response.raw_body)	
  	if 'acctId' in values:
  		return values['acctId']
  	return None

def getInfoBySummonerId(accountId):
   	response = unirest.get("https://community-league-of-legends.p.mashape.com/api/v1.0/EUNE/summoner/getAllPublicSummonerDataByAccount/%s" % accountId,
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




from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.datasets 			 import SupervisedDataSet

from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal



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


	return render(request, 'LeaguePredictor/neural.html' , my_hash )