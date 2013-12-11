import json
import unirest
import re
import logging
import time
import globals
from functools import wraps

API_KEY = "LPr5tiP2Bv4EdDJ7UDaoXghst0DkJBLC"
# Ralph Key API_KEY = "oLnuKcY8wryIkrE94xUMtGXjAbujt2Hx"
# Dimitry Key API_KEY = "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"

REGION = "EUW"
API_DOMAIN = "https://community-league-of-legends.p.mashape.com/api/v1.0/%s/summoner/" % REGION


logger = logging.getLogger(__name__)
def retry(ExceptionToCheck, tries=8, delay=1, backoff=2, logger=logger):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):       
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1                    
            return None
        return f_retry  # true decorator

    return deco_retry     
 
@retry(Exception)        
def getSummonerIdByAccountId(account_id):    
    method = 'getAllPublicSummonerDataByAccount'
    values = get_data(method, account_id) 
    try:
        return values["summoner"]["sumId"]
    except KeyError, e:
        log_error(e, method, account_id)
        raise KeyError


@retry(Exception ) 
def getAccountIdBySummonerId(summoner_id):
    method = 'getSummonerBySummonerId'
    values = get_data(method, summoner_id)
    try:
        name = values["array"][0] 

    except KeyError, e:
        log_error(e, method, summoner_id)
        raise KeyError
    
    accountid = getAccountIdByName(name) 
     
    return accountid
@retry(KeyError) 
def getNameByAccountId(account_id):
    method = 'getAllPublicSummonerDataByAccount'
    values = get_data(method, account_id)
    try:
        name = values["summoner"]["internalName"] 

    except KeyError, e:
        log_error(e, method, account_id)
        raise KeyError
    
    accountid = getAccountIdByName(name) 
     
    return accountid


@retry(Exception )
def getAccountIdByName(name):
    method = 'getSummonerByName'
    name = re.sub(r'\s+', '', name)
    name = unicode_conversion(name);
    values = get_data(method, name)
    try:
        return values['acctId']
    except KeyError,e:
        log_error(e, method, name)
        raise KeyError


@retry(Exception )        
def getRecentGamesByAccountId(account_id):
    method = 'getRecentGames'
    values = get_data(method, account_id)
    try:
        return values["gameStatistics"]["array"]
    except KeyError,e:
        log_error(e, method, account_id)
        raise KeyError


@retry(Exception )  
def getAggregatedStatsByAccountID(account_id):
    method = 'getAggregatedStats'
    values = get_data(method, account_id)
    try:
        return values["lifetimeStatistics"]["array"]
    except KeyError, e:        
        log_error(e, method, account_id)
        raise KeyError


@retry(Exception)         
def getLeagueForPlayerBySummonerID(summoner_ID):
    method = 'getLeagueForPlayer'
    values = get_data(method, summoner_ID)
    try:
        values['requestorsRank']
        return values
    except KeyError, e:  
        log_error(e, method, summoner_ID)
        raise KeyError 

@retry(KeyError)         
def retrieveInProgressSpectatorGameInfo(summonerName):
    method = 'retrieveInProgressSpectatorGameInfo'
    values = get_data(method, summonerName)
    try:
        values['game']
        return values
    except KeyError, e:  
        log_error(e, method, summonerName)
        raise KeyError 

# Helper functions

def log_error(error, method, argument):
    logger.error("%s(%s) : %s" % (method, error, argument))


def get_data( method, parameters):
    url = "%s%s/%s" % (API_DOMAIN, method, parameters);   
    response =  unirest.get(url.encode('utf-8'),
    headers={
        "X-Mashape-Authorization": API_KEY
        },
    encoding='utf-8',
    timeout=20000
        );  
    try:
        s= response.raw_body.replace('\\', '')        
        a= json.loads(s)
    except Exception, e:
        log_error("get_data", method, s)
        print s
        raise e
    return a


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