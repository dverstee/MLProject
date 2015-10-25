
def print_summoner(summoner, updated, realupdate):
    try:
        if updated:
            if realupdate:
                print "Summoner %s updated(accountId=%s) " % (summoner.name, summoner.account_id)
            else:
                print "No update was required for Summoner %s (accountId=%s) " % (summoner.name, summoner.account_id)
        else:
            print "Summoner %s added(accountId=%s) " % (summoner.name, summoner.account_id)
    except:
        pass


def print_champion_played(summoner, updated):
    try:
        if updated:
            print "champions for summoner %s updated(accountId=%s) " % (summoner.name, summoner.account_id)
        else:
            print "No need to update champions for summoner %s (accountId=%s) " % (summoner.name, summoner.account_id)
    except Exception:
        return None


def print_match(match):
    print match
