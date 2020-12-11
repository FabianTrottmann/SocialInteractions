import networkx
import pandas as pd
import matplotlib.pyplot as plt
from DataPreparer import DataPreparer
from NetworkDrawer import NetworkDrawer
from ComparisonOption import ComparisonOption

with open("./data/filter_clubs_top_7.txt", "r") as file:
    clubs = list(file)
topClubs = [x.strip() for x in clubs]
clubs = topClubs
preparer = DataPreparer()

# interaction part: ---
clubToCompare = "FC Basel"
season = "2013-2020"
minFee = 0
comparisonOption = ComparisonOption.TransferRatio
# ----------------------

clubToCompare = clubToCompare.split(";")

if len(clubToCompare) > 0:
    for club in clubToCompare:
        clubs.append(club)

print("choosen options:\n"
      "\ntop clubs: ", topClubs,
      " \ncompare club: ", clubToCompare,
      "\nseasons: ", season,
      "\nminFee: ", str(minFee))

if comparisonOption == ComparisonOption.TransferIncome:
    df, transferByClub = preparer.GetClubToClubTransferIncome(minFee, season, clubs)
elif comparisonOption == ComparisonOption.TransferExpense:
    df, transferByClub = preparer.GetClubToClubTransferExpense(minFee, season, clubs)
elif comparisonOption == ComparisonOption.TransferRatio:
    df, transferByClub = preparer.GetClubToClubTransferRatio(minFee, season, clubs)

for club in clubToCompare:
    value = transferByClub[club] if club in transferByClub else "NA"
    print(f"value for {club}: {value}")

drawer = NetworkDrawer()
drawer.Draw(df, clubToCompare, transferByClub)

# todo: OPTIONAL community möglichkeiten?
# todo: RestAPI and UI for Input and Result visualization
# todo: coords: set coords for compare clubs specifically
# todo: add missing nodes (bspw. ist AFC Ajax nicht vorhanden!, vermutlich weil nur outdegrees!)  absent nodes!!!!!
# todo: comparison options: additional transfer expense and transfer income (ratio already done)
# info: comparison of transfer income / expense https://www.transfermarkt.ch/statistik/einnahmenausgaben
# use case: e.g. Paris SG, at what specific time, was Paris SG bought by rich guys? (compare season before and after witch comparison option transfer expense)
# https://gephi.org/
# https://en.wikipedia.org/wiki/Rich-club_coefficient
