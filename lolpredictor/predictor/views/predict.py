from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer, BiasUnit
from pybrain.structure           import FullConnection, FeedForwardNetwork, LinearLayer, SigmoidLayer

from django.shortcuts import render
import itertools, collections
import logging
import pickle
import json
from util import getBasicDatafromMatch, getMinimalDatafromMatch
from lolpredictor.predictor.models import Match
import globals
logger = logging.getLogger(__name__)

def predict(request):    
    print "Predicting !"

    if request.method == 'GET':
        return render(request, 'predictor/predictor.html')

   

def log_debug(dimension , number_of_hidden_nodes, weightdecay,trnresult,tstresult):
    logger.debug(";%s; %s; %s; %s;%s" % (dimension,number_of_hidden_nodes, weightdecay, trnresult ,tstresult ))
    print ";%s; %s; %s; %s;%s" % ( dimension , number_of_hidden_nodes, weightdecay, trnresult ,tstresult )





def getdata(do_preprocessing, full_data):
    '''
    fetch and format the match data according to the given flags
    do_preprocessing: bool: true if preprocessing needs to be do_preprocessing
    full_data: bool: false if the minimal data should be used
    '''
    if full_data == 0 :
        fn = getMinimalDatafromMatch
    else:
        fn = getBasicDatafromMatch
    if globals.use_saved_data:
        try:
            with open('processed_data%d' % full_data) as outfile:
                data = json.load(outfile)
        except IOError:
            matches = Match.objects.all()
            data = map(lambda x: (fn(x,do_preprocessing), x.won), matches )
            with open('processed_data%d' % full_data, 'w') as outfile:
                json.dump(data,outfile)
    else:
        matches = Match.objects.all()
        data = map(lambda x: (fn(x,do_preprocessing), x.won), matches )
        with open('processed_data%d' % full_data, 'w') as outfile:
                json.dump(data,outfile)

    all_data = None
    for input, won in data:           
            if all_data is None:
                all_data = ClassificationDataSet(len(input), 1, nb_classes=2)       
            all_data.addSample(input, won)
    return all_data

def basicneuralnetwork(number_of_hidden_nodes,weightdecay, layers, alldata):
    '''
    This is a dataset 
    first argument is the dimension of the input
     second argument is dimension of the output
    '''  
    nr_of_iterations = 5


    

    # Construct neural network
    print "Constructing network"
    

    print "  (number_of_hidden_nodes : %s, weight decay : %s, layers: %s)" % (number_of_hidden_nodes, weightdecay, layers)

    train_results   = []
    test_results    = []
    neural_networks = []
    for i in  xrange(1,nr_of_iterations+1):
        print "Iteration %d" % i

        # Prepare the data
        tstdata, trndata = alldata.splitWithProportion( 0.15 )
        trndata._convertToOneOfMany()
        tstdata._convertToOneOfMany()
        # construct a neural network
        fnn = construct_neural_network(number_of_hidden_nodes, layers, trndata.indim, trndata.outdim)
        trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=False, weightdecay=weightdecay)
        #early stopping validation set = 0.25
        trainer.trainUntilConvergence(continueEpochs=5)   
        train_results.append(percentError( trainer.testOnClassData(), trndata['class'] ))
        test_results.append(percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] ))
        neural_networks.append(fnn)
        log_debug(trndata.indim,number_of_hidden_nodes, weightdecay,train_results[-1],test_results[-1])         
            
    # Compute means
    mean_train_error    = sum(train_results)/len(train_results)
    mean_test_error     = sum(test_results)/len(test_results)

    # Compute optimal network configuration
    optimal_test_error  = min(test_results)
    optimal_index       = test_results.index(optimal_test_error)

    # Save the optimal configuration to the file system
    neuralnetwork = 'neuralHiddenNode%sdecay%s'%(number_of_hidden_nodes, weightdecay)
    fileObject = open(neuralnetwork, 'w')
    pickle.dump(neural_networks[optimal_index], fileObject)
    fileObject.close()

    return (mean_train_error, mean_test_error)


def construct_neural_network(number_of_hidden_nodes, number_of_hidden_layers, inputdim, outputdim):
    """
    Constructs a neural network with a given amount of hidden layers and nodes per hidden layer
    """
    input_layer = LinearLayer(inputdim)
    hidden_layers = []
    output_layer = SoftmaxLayer(outputdim)
    # Nodes of the neural network
    fnn = FeedForwardNetwork()
    fnn.addInputModule(input_layer)
    for i in range(number_of_hidden_layers):
        sigm = SigmoidLayer(number_of_hidden_nodes)
        hidden_layers.append(sigm)
        fnn.addModule(sigm)
    fnn.addOutputModule(output_layer)
    bias = BiasUnit()
    fnn.addModule(bias)
    # Connections of the neural network
    input_connection = FullConnection(input_layer, hidden_layers[0])
    fnn.addConnection(input_connection)
    fnn.addConnection(FullConnection(bias, hidden_layers[0]))
    for i in range(len(hidden_layers) - 1):
        full = FullConnection(hidden_layers[i], hidden_layers[i+1])
        fnn.addConnection(full)
        fnn.addConnection(FullConnection(bias, hidden_layers[i+1]))
    output_connection = FullConnection(hidden_layers[-1], output_layer)
    fnn.addConnection(output_connection)
    fnn.addConnection(FullConnection(bias, hidden_layers[0]))
    fnn.sortModules()
    return fnn
