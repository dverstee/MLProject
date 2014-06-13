import json
import unirest
import re
import logging
import time
import globals
from functools import wraps

API_KEY = "72e5f115-6e76-43e2-8e95-af65ce16445d"
# Ralph Key API_KEY = "oLnuKcY8wryIkrE94xUMtGXjAbujt2Hx"
# Dimitry Key API_KEY = "rdhin8bBPEAPK5d5tcDxl94ygpAhUBLO"

REGION = "euw"
API_DOMAIN = "https://euw.api.pvp.net/api/lol/" 

NR_REQUEST=0

logger = logging.getLogger(__name__)
def retry(ExceptionToCheck, tries=3, delay=1, backoff=2, logger=logger):
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
                    y = f(*args, **kwargs)                                     
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)                    
                    time.sleep(mdelay)
                    mtries -= 1
                try:                   
                    if(y["status"] ["status_code"]==400):                                             
                        return 400 
                    if(y["status"] ["status_code"]==401):                                             
                        return 401
                    if(y["status"] ["status_code"]==429):
                        print("max number of api requests.")
                        mtries -= 1
                        time.sleep(5)
                        if mtries == 1:
                            time.sleep(10)
                        if mtries == 0:
                            return 429
                        
                    if(y["status"] ["status_code"]==500):
                        return 500    
                    if(y["status"] ["status_code"]==503):                                             
                        return 503
                    return y
                except Exception, e:                     
                    pass              
                try:
                    return y
                except UnboundLocalError, e:                     
                    mtries -= 1 

            return None
        return f_retry  # true decorator

    return deco_retry     
        




@retry(Exception)
def getSummonersByName(name):
    method = 'summoner/by-name/'
    version = "v1.4"
    appendix=""
    name = re.sub(r'\s+', '', name)
    name = unicode_conversion(name);
    values = get_data(method, name,version,appendix)
    name =name.lower()
    try:
        return values
    except KeyError,e:
        log_error(e, method, name)
        raise KeyError

@retry(Exception)  
def getAggregatedStatsById(id):
    method = 'stats/by-summoner/'
    version = "v1.3"
    appendix="/ranked"
    values = get_data(method,id,version,appendix)
    try:
        return values["champions"]
    except KeyError, e: 
        log_error(e, method, id)
        raise KeyError

@retry(Exception)  
def getRecentGamesById(id):    
    method = 'game/by-summoner/'
    version = "v1.3"
    appendix="/recent"
    values = get_data(method,id,version,appendix)
    try:        
        return values["games"]
    except KeyError, e:    
        print("error")       
        log_error(e, method, id)
        raise KeyError

@retry(Exception)  
def getLeagueForPlayerById(id):
    method = 'league/by-summoner/'
    version = "v2.4"
    appendix="/entry"
    values = get_data(method,id,version,appendix)    
    try:
        return values
    except KeyError, e:
        log_error(e, method, id)
        raise KeyError

@retry(Exception)  
def getSummonerById(id):
    method = 'summoner/'
    version = "v1.4"
    appendix=""
    values = get_data(method,id,version,appendix)    
    try:
        return values
    except KeyError, e:
        log_error(e, method, id)
        raise KeyError


# Helper functions

def log_error(error, method, argument):
    logger.error("%s(%s) : %s" % (method, error, argument))


def get_data(method, parameters,version,appendix):
    url = "%s%s/%s/%s%s%s?api_key=%s" % (API_DOMAIN,REGION,version,method,parameters,appendix,API_KEY);   
    print(url)
    response =  unirest.get(url.encode('utf-8'),    
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