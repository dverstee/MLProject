import datetime
from  lolpredictor.predictor.models import *
from  lolpredictor.predictor.views.api import *
from django.test import TestCase


class TestAPI(TestCase):
    def setUp(self):
        pass

    def testGetSummonersByName(self):
        name = "steeltje3"
        result = getSummonersByName(name)
        self.assertEqual(result[name]["id"],22933072)
    def testGetSummonersById(self):
        names = ["steeltje3","gezapigeeland","xindronke"]
        testnames=[]
        print ', '.join(names)        
        summoners = getSummonersByName(', '.join(names))        
        ids = []
        for name in names:
            ids.append(summoners[name]["id"])
        summoners = getSummonerById(str(','.join(str(v) for v in ids)))
        for id in ids:
            testnames.append(summoners[str(id)]["name"].lower())
        self.assertEqual(testnames,names)

