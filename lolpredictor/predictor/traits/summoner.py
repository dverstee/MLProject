from django.utils import timezone
from datetime import timedelta, datetime
from lolpredictor.predictor.models.summoner import Summoner
from lolpredictor.predictor.views.api import getLeagueForPlayerById, getSummonerById
from lolpredictor.predictor.config import config
from lolpredictor.predictor.enums import Tier, Division


def store_summoners(summoner_ids, region):

    updated_at_lower_bound = timezone.now() - timedelta(seconds=config.REFRESH_SUMMONER_INTERVAL)

    # Fetch the requested summoners which were already updated after the threshold
    summoners = Summoner.objects.filter(summoner_id__in=summoner_ids)
    summoners_dict = {summoner.account_id: summoner for summoner in summoners}

    # The ids which were already updated recently, skip these
    excluded_summoners = set \
        (map(lambda x: x.account_id, filter(lambda x: x.updated_at > updated_at_lower_bound, summoners)))

    # Api call to fetch the league information for the summoner id's
    leagues = getLeagueForPlayerById(','.join(str(v) for v in summoner_ids if v not in excluded_summoners))

    for account_id in summoner_ids:
        if account_id not in excluded_summoners:
            if account_id in summoners_dict.keys():
                summoner = summoners_dict[account_id]
            else:
                summoner_info = getSummonerById(account_id)
                summoner = Summoner.objects.create(**{
                    'summoner_id': account_id,
                    'name': summoner_info[str(account_id)]["name"],
                    'updated_at': datetime.now(),
                    'tier': 0,
                    'rank': 0,
                    'hotstreak': False

                })

            league_information = leagues[str(account_id)]

            print league_information

            for league in league_information:
                if league["queue"] == "RANKED_SOLO_5x5":
                    entries = league["entries"]
                    summoner.tier = Tier[league["tier"]].value
                    for entry in entries:
                        summoner.rank = Division[entry["division"]].value
                        summoner.name = entry["playerOrTeamName"]
                        summoner.hotstreak = entry["isHotStreak"]

            summoner.save()


    for summoner in summoners:
        print summoner
    return True