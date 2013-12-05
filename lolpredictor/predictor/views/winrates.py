import globals
import re
from lolpredictor.predictor.models import *
def winrates(request):
	for i in globals.junglematchups:
		image = i["image"]
		start_index=image.find('champions/')
		end_index=image.find('_32.png')
		champion_id = int(image[start_index+10:end_index])
		i["id"] = champion_id

	for i in globals.junglematchups:
		champion_1 = Champion.objects.get(pk=i["id"])
		for index in range(len(i["dataColor"])):
			id2 = globals.junglematchups[index]["id"]
			champion_2 = Champion.objects.get(pk=id2)
			try:
				matchup = Matchup.objects.get(champion_1=champion_1, champion_2=champion_2)
			except:
				new_matchup = Matchup.objects.create(champion_1=champion_1, champion_2=champion_2, win_rate=i["dataColor"][index])
				print new_matchup


