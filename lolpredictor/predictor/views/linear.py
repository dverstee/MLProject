from django.shortcuts import render
import logging
import json

from lolpredictor.predictor.models import *

logger = logging.getLogger(__name__)
activation_samples = []


def linear(request):
    print "Start preprocessing"
    # runpreprocessing()
    print "Starting LR "
    my_hash = {}
    options = []
    for field in PreProcessedMatch._meta.fields:
        fieldstring = str((str(field).split(".")[2]).replace("'", ""))
        print  fieldstring
        options.append(fieldstring)

    b = json.dumps(options)

    my_hash["dataset"] = determineevaluationfunction()
    my_hash["options"] = b
    return render(request, 'predictor/linearregression-Response.html', my_hash)


def determineevaluationfunction():
    matches = PreProcessedMatch.objects.all()[:5]
    my_hash = {}
    element = []
    dataset = []
    for match in matches:
        # TODO make this dynamic
        element = [int(match.team_1_top_score), int(match.team_2_top_score), int(match.won)]
        dataset.append(element)

    return dataset
