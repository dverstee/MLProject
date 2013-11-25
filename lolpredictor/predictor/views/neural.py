from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from django.shortcuts import render

from util import getDatafromMatch
from lolpredictor.predictor.models import match

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
        #   input = getDatafromMatch(matc)      
        #   alldata.addSample(input, matc.won)     
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
def preprocessingChampionPlayed(request):   

    #Preprocessing 
    champsplayed = ChampionPlayed.objects.all()
    nr=0
    kills=0
    deaths=0
    assits=0
    gold=0

    for cp in champsplayed:
        nr = nr +  cp.nr_gameswithchamp
        kills = kills + cp.average_kills
        deaths =deaths + cp.average_deaths
        assits=assits + cp.average_assists
        gold=gold + cp.average_gold

    nr = nr /len(champsplayed)
    kills = kills /len(champsplayed)
    deaths =deaths /len(champsplayed)
    assits=assits/len(champsplayed)
    gold=gold /len(champsplayed)
