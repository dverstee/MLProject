import json
import unirest
import re
import logging

API_KEY = "oLnuKcY8wryIkrE94xUMtGXjAbujt2Hx"
REGION = "EUW"
API_DOMAIN = "https://community-league-of-legends.p.mashape.com/api/v1.0/%s/summoner/" % REGION

logger = logging.getLogger(__name__)

def getSummonerIdByAccountId(account_id):    
    method = 'getAllPublicSummonerDataByAccount'
    values = get_data(method, account_id) 
    try:
        return values["summoner"]["sumId"]
    except KeyError, e:
        log_error(e, method, account_id)

def getAccountIdBySummonerId(summoner_id):
    method = 'getSummonerBySummonerId'
    values = get_data(method, summoner_id)
    try:
        name = values["array"][0]        
    except KeyError, e:
        log_error(e, method, summoner_id)
        return None

    accountid = getAccountIdByName(name)
     
    return accountid
def getAccountIdByName(name):
    method = 'getSummonerByName'
    name = re.sub(r'\s+', '', name)
    name = unicode_conversion(name);
    values = get_data(method, name)
    try:
        return values['acctId']
    except KeyError,e:
          log_error(e, method, name)

# def getInfoByaccountId(account_id):
#     method = 'getAllPublicSummonerDataByAccount'
#     values = get_data(method, account_id)
#     try:
#         return values
#     except KeyError,e:
#         log_error(e, method)

def getRecentGamesByAccountId(account_id):
    method = 'getRecentGames'
    values = get_data(method, account_id)
    try:
        return values["gameStatistics"]["array"]
    except KeyError,e:
        log_error(e, method, account_id)
        

def getAggregatedStatsByAccountID(account_id):
    method = 'getAggregatedStats'
    values = get_data(method, account_id)
    try:
        return values["lifetimeStatistics"]["array"]
    except KeyError, e:
        log_error(e, method)

def getLeagueForPlayerBySummonerID(summoner_ID):
    method = 'getLeagueForPlayer'
    values = get_data( method, summoner_ID)
    try:
        values['requestorsRank']
        return values
    except KeyError, e:        
        log_error(e, method, summoner_ID)

# Helper functions

def log_error(error, method, argument):
    logger.error("%s(%s) : %s" % (method, argument, url))


def get_data( method, parameters):
    url = "%s%s/%s" % (API_DOMAIN, method, parameters);
    # print url
    response =  unirest.get(url.encode('utf-8'),
    headers={
        "X-Mashape-Authorization": API_KEY
        },
    encoding='utf-8'
        );
    return json.loads(response.raw_body)

def unicode_conversion(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import htmlentitydefs
            entity = htmlentitydefs.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return unicode(entity, "iso-8859-1")
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)