from  lolpredictor.predictor.models import *

from django.shortcuts import render

def test(request):
	for match in Match.objects.all():
		sort_match_champions(match.match_id)
	return render(request, 'predictor/neural.html'  )
# Sort the list of the champions according to
# most probable position
def sort_match_champions(match_id):

	try:
		my_match = Match.objects.get(pk=match_id)
	except Error as e:
		# Match does not exist
		print e
		return None

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
	print "Match %s sorted:" % my_match.match_id
	print "  Team1 : %s" % optimal_setup_1
	print "  Team2 : %s" % optimal_setup_2
	my_match.save()


def sort_champion_list(champion_list, current_setup):
	current_champs = len(current_setup)
	# A setup has been found
	if current_champs == 5:
		return current_setup
	valid_champions = [champion for champion in champion_list if current_champs in classify(champion.champion) ]
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
	if(number_of_not_none(optimal_setup) == 5):
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





	