from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer



from django.shortcuts import render
import itertools, collections
import logging
import pickle
from util import getBasicDatafromMatch
from util import getMinimalDatafromMatch
from lolpredictor.predictor.models import Match
import globals
logger = logging.getLogger(__name__)

def neural(request):    
    matches = Match.objects.all()
    print "Number of matches in db : " 
    print  len(matches)
    

    weightdecaymax = 6 
    alldata = getdata(False)
    buildbestneuralnetwork(40,0.01,alldata)

    #sweep over all parameters to find the one that have the best mean performance
    for number_of_hidden_node in xrange(20,400,20):       
        for decay in xrange(1,weightdecaymax,1):
            weightdecay = 10**(-decay)            
            basicneuralnetwork(number_of_hidden_node,weightdecay,alldata)

    #build the best network with the parameters that performed best on mean
    buildbestneuralnetwork(globals.best_number_of_hidden_nodes,globals.best_weight_decay,alldata)        
   
    #alldata = getMinimaldata()    
    #for number_of_hidden_node in xrange(20,1000,20):       
    #    basicneuralnetwork(number_of_hidden_node,weightdecay,alldata)
    
    #print "epoch: %4d" %trainer.totalepochs
    #print "  train error: %5.2f%%" %trnresult
    #print "  test error: %5.2f%%" %tstresult
    
    

def log_debug(dimension , number_of_hidden_nodes, weightdecay,trnresult,tstresult):
    logger.debug(";%s; %s; %s; %s;%s" % (dimension,number_of_hidden_nodes, weightdecay, trnresult ,tstresult ))
    print ";%s; %s; %s; %s;%s" % ( dimension , number_of_hidden_nodes, weightdecay, trnresult ,tstresult )


def getMinimaldata():
    matches = match.objects.all()
    init=True
    for matc in matches:    
        
        if init:
            input = getMinimalDatafromMatch(matc,True)
            dimensions = len(input)
            print dimensions
            alldata = ClassificationDataSet(dimensions, 1, nb_classes=2)     
            alldata.addSample(input, matc.won) 
            init = False           
        else :       
            input = getMinimalDatafromMatch(matc,True)      
            alldata.addSample(input, matc.won)
            dimensions = len(input)
    return alldata

def getdata(Preprocessing):
    matches = Match.objects.all()
    init=True

    for matc in matches:    
        
        if init:
            input = getBasicDatafromMatch(matc,Preprocessing)
            dimensions = len(input)
            print dimensions
            alldata = ClassificationDataSet(dimensions, 1, nb_classes=2)     
            alldata.addSample(input, matc.won) 
            init = False  
            print input       
        else :       
            input = getBasicDatafromMatch(matc,Preprocessing)      
            alldata.addSample(input, matc.won)
            dimensions = len(input)
    return alldata

def basicneuralnetwork(number_of_hidden_nodes,weightdecay, alldata):

   
    #This is a dataset 
    #first argument is the dimension of the input
    # second argument is dimension of the output
    
   
  
    trnresult=0
    tstresult=0
    nr_of_iterations = 25

    tstdata, trndata = alldata.splitWithProportion( 0.25 )

    trndata._convertToOneOfMany( )
    tstdata._convertToOneOfMany( )       

    print "number_of_hidden_nodes : %s; weight decay : %s" % (number_of_hidden_nodes, weightdecay)
    #First  arggument is number of  inputs.
    #Second argument is number of hidden nodes 
    #Third is number of outputs

    for i in  xrange(1,nr_of_iterations,1):
        print i
        fnn = buildNetwork( trndata.indim, number_of_hidden_nodes, trndata.outdim, outclass=SoftmaxLayer )
        trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=False, weightdecay=weightdecay)
        #early stopping validation set = 0.25
        trainer.trainUntilConvergence(continueEpochs=5) 
        trnresult = trnresult + percentError( trainer.testOnClassData(), trndata['class'] )
        tstresult = tstresult + percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )
       

    trnresult =trnresult/nr_of_iterations
    tstresult = tstresult/nr_of_iterations

    if globals.best_error_rate > tstresult : 
        globals.best_error_rate = tstresult
        globals.best_weight_decay = weightdecay
        globals.best_number_of_hidden_nodes = number_of_hidden_nodes

  

    my_hash = {}
    my_hash["tstresult"] = tstresult
    my_hash["trnresult"] = trnresult

    log_debug(trndata.indim,weightdecay, weightdecay,trnresult,tstresult)
    
    return my_hash


def buildbestneuralnetwork(number_of_hidden_nodes,weightdecay, alldata):
    trnresult=0
    tstresult=0
    nr_of_iterations = 25

    tstdata, trndata = alldata.splitWithProportion( 0.25 )

    trndata._convertToOneOfMany( )
    tstdata._convertToOneOfMany( )         

    print "number_of_hidden_nodes : %s; weight decay : %s" % (number_of_hidden_nodes, weightdecay)
    #First  arggument is number of  inputs.
    #Second argument is number of hidden nodes 
    #Third is number of outputs
    bestresult = 100
    for i in  xrange(1,nr_of_iterations,1):
        print i
        fnn = buildNetwork( trndata.indim, number_of_hidden_nodes, trndata.outdim, outclass=SoftmaxLayer )
        trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=False, weightdecay=weightdecay)
        #early stopping validation set = 0.25
        trainer.trainUntilConvergence(continueEpochs=5)         
        trnresult = percentError( trainer.testOnClassData(), trndata['class'] )
        tstresult = percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )
        if tstresult < bestresult:
            #store network
            
            bestresult=tstresult
            fileObject = open('neural', 'w')
            pickle.dump(fnn, fileObject)
            fileObject.close()  
    
    print "best result  %s "% (bestresult)
    fileObject = open('neural','r')
    fnn = pickle.load(fileObject)
    trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=False, weightdecay=weightdecay)
    tstresult = percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )
    print  "check from loadednetwork: %s" % (tstresult)

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
