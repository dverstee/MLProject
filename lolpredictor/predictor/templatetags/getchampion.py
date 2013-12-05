from django import template

register = template.Library()

@register.assignment_tag
def getchampion(match, summoner):
    try:
        if match.team_1summoner1_id.summoner == summoner:
        	return match.team_1summoner1_id.champion
        elif match.team_1summoner2_id.summoner == summoner:
        	return match.team_1summoner2_id.champion
        elif match.team_1summoner3_id.summoner == summoner:
        	return match.team_1summoner3_id.champion
        elif match.team_1summoner4_id.summoner == summoner:
        	return match.team_1summoner4_id.champion
        elif match.team_1summoner5_id.summoner == summoner:
        	return match.team_1summoner5_id.champion
        elif match.team_2summoner1_id.summoner == summoner:
        	return match.team_1summoner1_id.champion
        elif match.team_2summoner2_id.summoner == summoner:
        	return match.team_1summoner2_id.champion
        elif match.team_2summoner3_id.summoner == summoner:
        	return match.team_1summoner3_id.champion
        elif match.team_2summoner4_id.summoner == summoner:
        	return match.team_1summoner4_id.champion
        elif match.team_2summoner5_id.summoner == summoner:
        	return match.team_1summoner5_id.champion
    except:
        return None