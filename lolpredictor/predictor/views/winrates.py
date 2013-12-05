import globals
import re
from lolpredictor.predictor.models import *
def winrates(request):
	for i in globals.botsynergy_adc:
		image = i["image"]
		start_index=image.find('champions/')
		end_index=image.find('_32.png')
		champion_id = int(image[start_index+10:end_index])
		i["id"] = champion_id
	for i in globals.botsynergy_support:
		image = i["image"]
		start_index=image.find('champions/')
		end_index=image.find('_32.png')
		champion_id = int(image[start_index+10:end_index])
		i["id"] = champion_id
	for i in globals.botsynergy_adc:
		champion_1 = Champion.objects.get(pk=i["id"])
		for index in range(len(i["dataColor"])):
			id2 = globals.botsynergy_support[index]["id"]
			champion_2 = Champion.objects.get(pk=id2)
			print champion_2
			print id2
			try:
				matchup = Synergy.objects.get(champion_1=champion_1, champion_2=champion_2)
				matchup.delete()
			except:
				pass
				# new_matchup = Synergy.objects.create(champion_1=champion_1, champion_2=champion_2, win_rate=i["dataColor"][index])
				# print new_matchup


