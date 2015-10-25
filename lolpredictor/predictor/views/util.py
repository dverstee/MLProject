#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from  lolpredictor.predictor.models import *
from datetime import *
from api import *
from django.db import IntegrityError
from preprocessing import *
import globals
from django.utils import timezone

logger = logging.getLogger(__name__)

REFRESH_SUMMONER_INTERVAL = 3600 * 24  # One day refresh interval
REFRESH_SUMMONER_CHALMPS_INTERVAL = 3600 * 4


def parse_champions(champions):
    parsed_list = []
    for key, champion in champions.items():
        champion_hash = {"id": champion["championId"],
                         "games": champion["totalGamesPlayed"],
                         "image": "https://github.com/rwarasaurus/league-of-legends-database/blob/master/icons/%d.jpg?raw=true" % \
                                  champion["championId"]}
        parsed_list.append(champion_hash)
    return parsed_list


def parse_ranked_games(games, id):
    recentadds = globals.nrgamesadded
    recenterrors = globals.nrerrors
    for game in games:
        if game["subType"] == "RANKED_SOLO_5x5":
            m = store_match(game, "RANKED_SOLO_5x5", id, "euw")
            if m is not None:
                globals.nrgamesadded += 1
            else:
                globals.nrerrors += 1

    if recentadds - globals.nrgamesadded == 0 and recenterrors - globals.nrerrors == 0:
        logger.debug("Not enough matches")
        print "Not enough matches"
        return None

    return globals.nrgamesadded


def store_match(game, type, summoner_id, region):
    our_summonersids = []
    their_summonersids = []
    all_ids = []
    our_team = []
    their_team = []
    championid = game["championId"]
    team_id = game["teamId"]
    match_id = game["gameId"]

    try:
        m = Match.objects.get(match_id=match_id)
        print "This match was already stored"
        globals.nrofupdates += 1
        return m
    except Match.DoesNotExist, e:
        pass

    our_summonersids.append(summoner_id)
    fellowplayers = game["fellowPlayers"]
    for player in fellowplayers:
        if player["teamId"] == team_id:
            our_summonersids.append(player["summonerId"])
        else:
            their_summonersids.append(player["summonerId"])
    all_ids = our_summonersids + their_summonersids
    store_summoners(all_ids, region)
    print("stored summoners")

    champion = Champion.objects.get(pk=championid)
    store_champions_played(id, champion)

    try:
        summoner = Summoner.objects.get(summoner_id=summoner_id)
        champPlayed = ChampionPlayed.objects.get(summoner=summoner, champion=champion)
    except ChampionPlayed.DoesNotExist:
        print "Exception DoesNotExist 1"
        return None

    our_team.append(champPlayed)
    # Store Others
    fellowplayers = game["fellowPlayers"]
    for player in fellowplayers:
        champion_id = player["championId"]
        summoner_id = player["summonerId"]
        try:
            champion = Champion.objects.get(pk=champion_id)
        except Champion.DoesNotExist:
            print champion_id
        try:
            store_champions_played(summoner_id, champion)
        except KeyError, e:
            print "Error storing champions"
            return None
        try:
            summoner = Summoner.objects.get(summoner_id=summoner_id)
            champion_played = ChampionPlayed.objects.get(summoner=summoner, champion=champion)
        except ChampionPlayed.DoesNotExist:
            print "Exception DoesNotExist 2"
            return None

        if player["teamId"] == team_id:
            our_team.append(champion_played)
        else:
            their_team.append(champion_played)

    if team_id == 100:
        team1_is_red = True
    else:
        team1_is_red = False
    # TODO : PREMADE size uitzoeken hoe het werkt.
    won = determineWin(game)
    premadesize = 0
    print("all summoners and champions played stored")
    # TODO Iterate over the list to make the match object ! :)
    try:
        m = Match.objects.create(match_id=match_id, team1_is_red=team1_is_red, nr_premade_team1=premadesize,
                                 nr_premade_team2=premadesize, won=won, team_1summoner1_id=our_team[0],
                                 team_1summoner2_id=our_team[1], team_1summoner3_id=our_team[2],
                                 team_1summoner4_id=our_team[3], team_1summoner5_id=our_team[4],
                                 team_2summoner1_id=their_team[0], team_2summoner2_id=their_team[1],
                                 team_2summoner3_id=their_team[2], team_2summoner4_id=their_team[3],
                                 team_2summoner5_id=their_team[4], match_type=type)
        sort_match_champions(m.match_id)
        print_match(m)
    except IntegrityError as e:
        logger = logging.getLogger("Double matchid found")
        return None
    return m


def store_summoners(summoner_ids, region):

    updated_at_lower_bound = timezone.now() - timedelta(seconds=REFRESH_SUMMONER_INTERVAL)

    # Fetch the requested summoners which were already updated after the threshold
    summoners = Summoner.objects.filter(summoner_id__in=summoner_ids)
    summoners_dict = {summoner.account_id: summoner for summoner in summoners}

    # The ids which were already updated recently, skip these
    excluded_summoners = set(map(lambda x: x.account_id, filter(lambda x: x.updated_at > updated_at_lower_bound, summoners)))

    # Api call to fetch the league information for the summoner id's
    leagues = getLeagueForPlayerById(','.join(str(v) for v in summoner_ids if v not in excluded_summoners))

    for account_id in account_ids:
        if account_id not in excluded_summoners:
            if account_id in summoners_dict.keys():
                summoner = summoners_dict[account_id]
            else:
                summoner_info = getSummonerById(account_id)
                summoner = Summoner.objects.create(**{
                    'account_id': account_id,
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
                    summoner.tier = tiertoint(league["tier"])
                    for entry in entries:
                        summoner.rank = ranktoint(entry["division"])
                        summoner.name = entry["playerOrTeamName"]
                        summoner.hotstreak = entry["isHotStreak"]

            summoner.save()


    for summoner in summoners:
        print summoner
    return True


# Store the information for all champions for the given summoner
# return: false if the summoner was recently updated
def store_champions_played(id, champion):
    summoner = Summoner.objects.get(account_id=id)
    try:
        cp = ChampionPlayed.objects.get(summoner=summoner, champion=champion)
        if cp is not None:
            diff = datetime.now() - cp.champions_updated_at.replace(tzinfo=None) - timedelta(
                seconds=REFRESH_SUMMONER_INTERVAL)
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


def ranktoint(rank):
    if rank == "I":
        return 1
    elif rank == "II":
        return 2
    elif rank == "III":
        return 3
    elif rank == "IV":
        return 4
    elif rank == "V":
        return 5


def tiertoint(tier):
    if tier == "BRONZE":
        return 1
    elif tier == "SILVER":
        return 2
    elif tier == "GOLD":
        return 3
    elif tier == "PLATINUM":
        return 4
    elif tier == "DIAMOND":
        return 5


def determineWin(game):
    return game["stats"]["win"]


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
