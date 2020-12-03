import networkx
import pandas as pd
import matplotlib.pyplot as plt
from DataPreparer import DataPreparer
from NetworkDrawer import NetworkDrawer

with open("./data/filter_clubs_top_7.txt", "r") as file:
    clubs = list(file)
clubs = [x.strip() for x in clubs]

preparer = DataPreparer()

# ---- customize: -------
additionalClub = "AFC Ajax"
season = "2013-2020"
minFeeInMio = 2
# ----------------------

minFee = minFeeInMio * 1000000

if additionalClub:
    clubs.append(additionalClub)

df1, ratioByClub = preparer.GetClubFromClubToPair(minFee, season, clubs)
#df2 = preparer.GetClubFromNationsToPair(minMarketValue, seasonGreaterThan, clubs)

# todo: community möglichkeiten?
# todo: kann node size gemäss verhältniss (ausgaben / einnahmen gemacht werden)?
# todo: add missing nodes (bspw. ist AFC Ajax nicht vorhanden!, vermutlich weil nur outdegrees!)  absent nodes!!!!!
# todo: https://www.transfermarkt.ch/statistik/einnahmenausgaben

drawer = NetworkDrawer()
resizeNodesIndegree = False
resizeNodesOutdegree = False
drawer.Draw(df1, ratioByClub, resizeNodesIndegree, resizeNodesOutdegree)
