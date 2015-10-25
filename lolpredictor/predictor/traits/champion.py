

def parse_champions(champions):
    parsed_list = []
    for key, champion in champions.items():
        champion_hash = {"id": champion["championId"],
                         "games": champion["totalGamesPlayed"],
                         "image": "https://github.com/rwarasaurus/league-of-legends-database/blob/master/icons/%d.jpg?raw=true" % \
                                  champion["championId"]}
        parsed_list.append(champion_hash)
    return parsed_list