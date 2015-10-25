from  lolpredictor.predictor.models import *
from django.shortcuts import render
from django.db import IntegrityError


def test():
    return 0


# Runs the preprocessing again for all the matches

def runpreprocessing():
    print ("Deleting preprocessed data ...")
    PreProcessedMatch.objects.all().delete()
    print ("fetching data ...")
    matches = Match.objects.all()
    for match in matches:
        match = preprocessMatch(match, False)

    return 0


# Runs the preprocessing for a single match
def preprocessMatch(matc, reverse):
    # sorts the champions
    matc = sort_match_champions(matc)
    # Converts the champions into features depending on a some factors
    team_1_top_score = champion_played_to_features(matc.team_1summoner1_id)
    team_1_mid_score = champion_played_to_features(matc.team_1summoner2_id)
    team_1_adc_score = champion_played_to_features(matc.team_1summoner3_id)
    team_1_supp_score = champion_played_to_features(matc.team_1summoner4_id)
    team_1_jungle_score = champion_played_to_features(matc.team_1summoner5_id)

    team_2_top_score = champion_played_to_features(matc.team_2summoner1_id)
    team_2_mid_score = champion_played_to_features(matc.team_2summoner2_id)
    team_2_adc_score = champion_played_to_features(matc.team_2summoner3_id)
    team_2_supp_score = champion_played_to_features(matc.team_2summoner4_id)
    team_2_jungle_score = champion_played_to_features(matc.team_2summoner5_id)


    # Stores the preporcessed match
    try:
        m = PreProcessedMatch.objects.create(match_id=matc.match_id, team1_is_red=matc.team1_is_red,
                                             nr_premade_team1=matc.nr_premade_team1,
                                             nr_premade_team2=matc.nr_premade_team2,
                                             won=matc.won,
                                             team_1_top_score=team_1_top_score,
                                             team_1_mid_score=team_1_mid_score,
                                             team_1_adc_score=team_1_adc_score,
                                             team_1_supp_score=team_1_supp_score,
                                             team_1_jungle_score=team_1_jungle_score,
                                             team_2_top_score=team_2_top_score,
                                             team_2_mid_score=team_2_mid_score,
                                             team_2_adc_score=team_2_adc_score,
                                             team_2_supp_score=team_2_supp_score,
                                             team_2_jungle_score=team_2_jungle_score
                                             )


    except IntegrityError as e:
        print "Double matchid found"
        return None
    return input


# Sort the list of the champions according to
# most probable position
def sort_match_champions(my_match):
    team_1 = [my_match.team_1summoner1_id,
              my_match.team_1summoner2_id,
              my_match.team_1summoner3_id,
              my_match.team_1summoner4_id,
              my_match.team_1summoner5_id]
    team_2 = [my_match.team_2summoner1_id,
              my_match.team_2summoner2_id,
              my_match.team_2summoner3_id,
              my_match.team_2summoner4_id,
              my_match.team_2summoner5_id]
    optimal_setup_1 = fill_missing_spots(sort_champion_list(team_1, []), team_1)
    optimal_setup_2 = fill_missing_spots(sort_champion_list(team_2, []), team_2)

    (my_match.team_1summoner1_id,
     my_match.team_1summoner2_id,
     my_match.team_1summoner3_id,
     my_match.team_1summoner4_id,
     my_match.team_1summoner5_id) = optimal_setup_1
    (my_match.team_2summoner1_id,
     my_match.team_2summoner2_id,
     my_match.team_2summoner3_id,
     my_match.team_2summoner4_id,
     my_match.team_2summoner5_id) = optimal_setup_2
    # print "Match %s sorted:" % my_match.match_id
    # print "  Team1 : %s" % optimal_setup_1
    # print "  Team2 : %s" % optimal_setup_2
    return my_match


def sort_champion_list(champion_list, current_setup):
    current_champs = len(current_setup)
    # A setup has been found
    if current_champs == 5:
        return current_setup
    valid_champions = [champion for champion in champion_list if current_champs in classify(champion.champion)]
    best_solution = None
    for champion in valid_champions:
        result = sort_champion_list([x for x in champion_list if x != champion], current_setup + [champion])
        if best_solution is None or number_of_not_none(result) > number_of_not_none(best_solution):
            best_solution = result
    no_champ = sort_champion_list(champion_list, current_setup + [None])
    if best_solution is None or number_of_not_none(no_champ) > number_of_not_none(best_solution):
        best_solution = no_champ
    return best_solution


def fill_missing_spots(optimal_setup, champion_list):
    if (number_of_not_none(optimal_setup) == 5):
        return optimal_setup
    remaining_champions = [champion for champion in champion_list if not champion in optimal_setup]
    for i in range(5):
        if optimal_setup[i] is None:
            optimal_setup[i] = remaining_champions[0]
            remaining_champions = remaining_champions[1:]
    return optimal_setup


def number_of_not_none(list):
    return len(filter(None, list))


def classify(champion):
    roles = []
    if champion.can_top:
        roles.append(0)
    if champion.can_mid:
        roles.append(1)
    if champion.can_jungle:
        roles.append(2)
    if champion.can_adc:
        roles.append(3)
    if champion.can_support:
        roles.append(4)
    return roles


# TODO incorporate into model
def get_win_rates(match):
    winrates = []
    try:
        matchup = Matchup.objects.get(champion_1=match.team_1summoner1_id.champion,
                                      champion_2=match.team_2summoner1_id.champion)
        winrates.append(matchup.win_rate)
    except Matchup.DoesNotExist, e:
        winrates.append(0.5)
    try:
        matchup = Matchup.objects.get(champion_1=match.team_1summoner2_id.champion,
                                      champion_2=match.team_2summoner2_id.champion)
        winrates.append(matchup.win_rate)
    except Matchup.DoesNotExist, e:
        winrates.append(0.5)

    try:
        matchup = Matchup.objects.get(champion_1=match.team_1summoner3_id.champion,
                                      champion_2=match.team_2summoner3_id.champion)
        winrates.append(matchup.win_rate)
    except Matchup.DoesNotExist, e:
        winrates.append(0.5)

    try:
        matchup = Matchup.objects.get(champion_1=match.team_1summoner4_id.champion,
                                      champion_2=match.team_2summoner4_id.champion)
        winrates.append(matchup.win_rate)
    except Matchup.DoesNotExist, e:
        winrates.append(0.5)

    try:
        synergy = Synergy.objects.get(champion_1=match.team_1summoner4_id.champion,
                                      champion_2=match.team_2summoner4_id.champion)
        winrates.append(synergy.win_rate)
    except Synergy.DoesNotExist, e:
        winrates.append(0.5)
    return winrates


# Gets the champions played and converts them in a score #TODO put reasoning in conversion [ranking, kdr, normalized_gold] => score
def champion_played_to_features(champion_played):
    # print "%s : %d/%d/%d" % (champion_played.champion, champion_played.average_kills, champion_played.average_deaths, champion_played.average_assists)
    # 0 to 1 ranking
    # champion_played=ChampionPlayed.objects.get(pk=cp_id)
    ranking = float((champion_played.summoner.tier) - 1) / 5.0 + float(4 - (champion_played.summoner.rank - 1)) / 50.0
    if champion_played.average_deaths:
        kdr = float(champion_played.average_kills + champion_played.average_assists / 2) / float(
            champion_played.average_deaths)
    else:
        kdr = float(champion_played.average_kills + champion_played.average_assists / 2) * 1.5
    normalized_gold = float(champion_played.average_gold)
    return 1000 * ranking + 1000 * kdr + normalized_gold
