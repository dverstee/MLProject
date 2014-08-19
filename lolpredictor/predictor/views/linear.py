
from django.shortcuts import render
import itertools, collections
import logging
import pickle
import json
import os
from util import getBasicDatafromMatch, getMinimalDatafromMatch
from scipy.optimize import leastsq
from lolpredictor.predictor.models import Match
import numpy as np
from numpy import arange,array,ones,linalg
import globals
logger = logging.getLogger(__name__)
activation_samples =[]  
def linear(request):    
    print "Starting LR "
    d =   alldata = getdata(False, globals.use_full_features)
    determineevaluationfunction(d)

def determineevaluationfunction(darray):
    data =np.array(darray)      
    size = len(data[:,1])
    x= np.array([data[:,0], ones(size)] ) 
    y= np.array(data[:,1])
    print x
    xi = arange(0,9)
    A = array([ xi, ones(9)])
    y = [19, 20, 20.5, 21.5, 22, 23, 23, 25.5, 24]
    print A.shape
 
    w = np.linalg.lstsq(A.T,y)[0]
    print w
    print (x)
   
def getdata(do_preprocessing, full_data):
    '''
    fetch and format the match data according to the given flags
    do_preprocessing: bool: true if preprocessing needs to be do_preprocessing
    full_data: bool: false if the minimal data should be used
    '''
    print ("fetching data ...")
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
            data = map(lambda x: (fn(x,do_preprocessing,False), x.won), matches)
            data += map(lambda x: (fn(x,do_preprocessing,True), not x.won), matches)
            with open('processed_data%d' % full_data, 'w') as outfile:
                json.dump(data,outfile)
    else:
        matches = Match.objects.all()
        data = map(lambda x: (fn(x,do_preprocessing,False), x.won), matches)
        data += map(lambda x: (fn(x,do_preprocessing,True), not x.won), matches)
        with open('processed_data%d' % full_data, 'w') as outfile:
            json.dump(data,outfile)
    return data    