from lolpredictor.predictor.models import Match, ChampionPlayed, Champion, Summoner
from lolpredictor.predictor.traits.summoner import store_summoners
from lolpredictor.predictor.traits.champion_played import store_champions_played
from lolpredictor.predictor.utils.formatting import print_match
from lolpredictor.predictor.views.preprocessing import sort_match_champions
from django.db import IntegrityError


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
    won = game["stats"]["win"]
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
        return None
    return m


def parse_ranked_games(games, id):
    # recentadds = globals.nrgamesadded
    # recenterrors = globals.nrerrors
    nr_games_added = 0

    for game in games:
        if game["subType"] == "RANKED_SOLO_5x5":
            m = store_match(game, "RANKED_SOLO_5x5", id, "euw")
            if m is not None:
                pass
                # globals.nrgamesadded += 1
            else:
                pass
                # globals.nrerrors += 1
            nr_games_added += 1

    if nr_games_added == 0:
        print "Not enough matches"
        return None

    return nr_games_added
