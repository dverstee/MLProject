from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer



from django.shortcuts import render
import itertools, collections
import logging
from util import getBasicDatafromMatch
from lolpredictor.predictor.models import match
logger = logging.getLogger(__name__)

def neural(request):    
    matches = match.objects.all()
    print "Number of matches in db : " 
    print  len(matches)
    

    number_of_hidden_nodes = [ 20 , 40 ,80 ,100 ,200 ,500 ,1000]   
    number_of_training_epochs = 100
    iterator = number_of_hidden_nodes.__iter__()
    alldata = getdata()

    for number_of_hidden_node in iterator:       
        basicneuralnetwork(number_of_hidden_node,number_of_training_epochs,alldata)

    #print "epoch: %4d" %trainer.totalepochs
    #print "  train error: %5.2f%%" %trnresult
    #print "  test error: %5.2f%%" %tstresult
    
    figure(1)
    ioff()  # interactive graphics off
    clf()   # clear the plot
    hold(True) # overplot on
    for c in [0,1,2]:
        here, _ = where(tstdata['class']==c)
        plot(tstdata['input'][here,0],tstdata['input'][here,1],'o')
    if out.max()!=out.min():  # safety check against flat field
        contourf(X, Y, out)   # plot the contour
    ion()   # interactive graphics on
    draw()  # update the plot
    return render(request, 'predictor/neural.html'  )

def log_debug(number_of_hidden_nodes, number_of_training_epochs,trnresult,tstresult):
    logger.debug("%s, %s , %s , %s" % (number_of_hidden_nodes, number_of_training_epochs, trnresult ,tstresult ))
    print "%s, %s , %s , %s" % (number_of_hidden_nodes, number_of_training_epochs, trnresult ,tstresult )




def getdata():
    matches = match.objects.all()
    init=True
    for matc in matches:    
        
        if init:
            input = getBasicDatafromMatch(matc)
            dimensions = len(input)
            alldata = ClassificationDataSet(dimensions, 1, nb_classes=2)     
            alldata.addSample(input, matc.won) 
            init = False           
        else :       
            input = getBasicDatafromMatch(matc)      
            alldata.addSample(input, matc.won)
            dimensions = len(input)
    return alldata
def basicneuralnetwork(number_of_hidden_nodes,number_of_training_epochs, alldata):

   
    #This is a dataset 
    #first argument is the dimension of the input
    # second argument is dimension of the output
    
    
    print number_of_hidden_nodes
    print number_of_training_epochs

   

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
    my_hash = {}
    my_hash["tstresult"] = tstresult
    my_hash["trnresult"] = trnresult

    log_debug(number_of_hidden_nodes, number_of_training_epochs,trnresult,tstresult)

    return my_hash

#def basicneuralnetworkpreprocessing():


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
