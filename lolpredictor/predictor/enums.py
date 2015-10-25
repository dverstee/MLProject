from enum import Enum


class Region(Enum):
    EUW = "euw"
    NA = "na"


class Tier(Enum):
    UNRANKED = 0
    BRONZE = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4
    DIAMOND = 5
    MASTER = 6


class Division(Enum):
    UNRANKED = 0
    V = 1
    IV = 2
    III = 3
    II = 4
    I = 5