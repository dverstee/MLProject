from lolpredictor.predictor.models import Summoner, ChampionPlayed, Champion
from datetime import timedelta, datetime
from lolpredictor.predictor.config import config
from lolpredictor.predictor.utils.formatting import print_champion_played
from lolpredictor.predictor.views.api import getAggregatedStatsById


def store_champions_played(id, champion):
    summoner = Summoner.objects.get(account_id=id)
    try:
        cp = ChampionPlayed.objects.get(summoner=summoner, champion=champion)
        if cp is not None:
            diff = datetime.now() - cp.champions_updated_at.replace(tzinfo=None) - timedelta(
                seconds=config.REFRESH_SUMMONER_INTERVAL)
            if diff.days < 0:
                print_champion_played(summoner, False)
                return False
    except:
        pass

    accountstats = getAggregatedStatsById(id)
    accountstats = accountstats["champions"]
    """TODO : rework
	 if	accountstats is None :
		print "Can't get accountstats"
		raise KeyError"""
    param_hash = {}
    for champion_stats in accountstats:
        champion_id = champion_stats["id"]
        # review
        if champion_id not in param_hash:
            param_hash[champion_id] = {}
        try:
            champion_instance = Champion.objects.get(pk=champion_id)
        except:
            continue

        param_hash[champion_id]["champion"] = champion_instance
        param_hash[champion_id]["summoner"] = summoner
        stats = champion_stats["stats"]

        param_hash[champion_id]["nr_gameswithchamp"] = stats["totalSessionsPlayed"]
        param_hash[champion_id]["average_assists"] = stats["totalAssists"]
        param_hash[champion_id]["average_deaths"] = stats["totalDeathsPerSession"]
        param_hash[champion_id]["average_kills"] = stats["totalChampionKills"]
        param_hash[champion_id]["average_gold"] = stats["totalGoldEarned"]
    for champion_id in param_hash:
        params = param_hash[champion_id]
        try:
            champion_instance = Champion.objects.get(pk=champion_id)
        except:
            continue
        try:
            champ_played = ChampionPlayed.objects.get(champion=champion_instance, summoner=summoner)
            champ_played.delete()
        except ChampionPlayed.DoesNotExist:
            pass
        params["average_assists"] = params["average_assists"] / params["nr_gameswithchamp"]
        params["average_deaths"] = params["average_deaths"] / params["nr_gameswithchamp"]
        params["average_kills"] = params["average_kills"] / params["nr_gameswithchamp"]
        params["average_gold"] = params["average_gold"] / params["nr_gameswithchamp"]

        c1 = ChampionPlayed.objects.create(**params)

    print_champion_played(summoner, True)
    return True
