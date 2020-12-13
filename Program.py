import networkx
import pandas as pd
import matplotlib.pyplot as plt
from DataPreparer import DataPreparer
from NetworkDrawer import NetworkDrawer
from ComparisonOption import ComparisonOption

 # interaction part: ---
league = "Bundesliga"
#season = "2014-2019"
season = "2000-2005"
# ----------------------

comparisonOption = ComparisonOption.TransferRatio
print("choosen options:\n"
      " \nleague: ", league,
      "\nseasons: ", season)

preparer = DataPreparer()
df, transferByClub = preparer.GetClubToClubTransferExpense(league, season)

drawer = NetworkDrawer()
drawer.Draw(df, transferByClub)


if False:
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


# https://gephi.org/
# https://en.wikipedia.org/wiki/Rich-club_coefficient
