import networkx
import pandas as pd
import matplotlib.pyplot as plt
from DataPreparer import DataPreparer
from NetworkDrawer import NetworkDrawer
from ComparisonOption import ComparisonOption

 # interaction part: ---
league = "Bundesliga"
season = "2000-2005"
# ----------------------

comparisonOption = ComparisonOption.TransferRatio
print("choosen options:\n"
      " \nleague: ", league,
      "\nseasons: ", season)

preparer = DataPreparer()
df, transferByClub = preparer.GetClubToClubTransferExpense(league, season)

preparer.GetClubToClubTransferExpense_CSV(league, season)

drawer = NetworkDrawer()
drawer.Draw(df, transferByClub)