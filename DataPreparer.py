import pandas as pd
import csv
import numpy as np

class DataPreparer:
    def GetClubToClubTransferExpense(self, league, season):
        dfTrans = self.__cleanLoadTransfers()
        dfTrans = self.__filterSeasons(dfTrans, 0, season)
        dfLeague = pd.read_csv("./data/dict_leagues.csv", sep=";", encoding="iso-8859-15")
        dfClubs = pd.read_csv("./data/clubs_in_leagues.csv", sep=";", encoding="iso-8859-15")
        idLeague = dfLeague[dfLeague["name"] == league]["id"].iloc[0]
        clubIds = dfClubs[dfClubs["league_id"] == int(idLeague)]["club_id"].unique()
        dfTrans = dfTrans[dfTrans["to_club_id"].isin(clubIds) | (dfTrans["from_club_id"].isin(clubIds))]
        fromExp = "{0}-Expenses".format(league)
        toIncome = "{0}-Income".format(league)

        dfTrans["from_club_name"] = dfTrans.apply(lambda row: fromExp if row["from_club_id"] not in clubIds else row["from_club_name"].strip(), axis=1)
        dfTrans["to_club_name"] = dfTrans.apply(lambda row: toIncome if row["to_club_id"] not in clubIds else row["to_club_name"].strip(), axis=1)
        #dfTrans["thickness"] = dfTrans.apply(lambda row: self.__GetThickness(dfTrans, row), axis=1)
        transferExpenseByClub = dfTrans.groupby(["to_club_name"]).agg({"fee": "sum"})["fee"].to_dict()
        transferExpenseByClub2 = dfTrans.groupby(["from_club_name"]).agg({"fee": "sum"})["fee"].to_dict()
        transferExpenseByClub[fromExp] = transferExpenseByClub2[fromExp]
        df = dfTrans[["from_club_name", "to_club_name"]]
        return df, transferExpenseByClub

    def GetClubToClubTransferExpense_CSV(self, league, season):
        dfTrans = self.__cleanLoadTransfers()
        dfTrans = self.__filterSeasons(dfTrans, 0, season)
        dfLeague = pd.read_csv("./data/dict_leagues.csv", sep=";", encoding="iso-8859-15")
        dfClubs = pd.read_csv("./data/clubs_in_leagues.csv", sep=";", encoding="iso-8859-15")
        idLeague = dfLeague[dfLeague["name"] == league]["id"].iloc[0]
        dfClubs = self.__filterSeasonClubs(dfClubs, season, idLeague)
        dfUniqueClubs = dfClubs[['club_id', 'club_name']].drop_duplicates()
        dfInOut = pd.DataFrame(columns=['club_id', 'club_name'], data=[[-1, 'Out'], [-2, 'In']])
        dfUniqueClubs = dfUniqueClubs.append(dfInOut)
        dfTrans.loc[~dfTrans['from_club_id'].isin(dfUniqueClubs['club_id']), 'from_club_id'] = -2
        dfTrans.loc[dfTrans['from_club_id'] == -2, 'from_club_name'] = 'In'
        dfTrans.loc[~dfTrans['to_club_id'].isin(dfUniqueClubs['club_id']), 'to_club_id'] = -1
        dfTrans.loc[dfTrans['to_club_id'] == -1, 'to_club_name'] = 'Out'



        dfLeagueKPI = dfClubs.groupby(['club_id', 'club_name']).agg(
            noOfLeagueTitles = pd.NamedAgg(column='is_champion', aggfunc='sum'),
            noOfCupTitles = pd.NamedAgg(column='is_cup_winner', aggfunc='sum'),
            medianPlace = pd.NamedAgg(column='place', aggfunc=np.median),
            avgPlace = pd.NamedAgg(column='place', aggfunc=np.average)

        )
        dfTransferOutKPI = dfTrans.groupby(['from_club_id', 'from_club_name']).agg(
                NoOutTransfers = pd.NamedAgg(column='from_club_id', aggfunc='count'),
                earnings = pd.NamedAgg(column='fee', aggfunc='sum')
                )
        dfTransferInKPI = dfTrans.groupby(['to_club_id', 'to_club_name']).agg(
                NoOutTransfers = pd.NamedAgg(column='to_club_id', aggfunc='count'),
                expenses = pd.NamedAgg(column='fee', aggfunc='sum')
                )

        dfUniqueClubs = pd.merge(left=dfUniqueClubs, right=dfTransferOutKPI, how='left', left_on='club_id', right_on='from_club_id')
        dfUniqueClubs = pd.merge(left=dfUniqueClubs, right=dfTransferInKPI, how='left', left_on='club_id', right_on='to_club_id')
        dfUniqueClubs = pd.merge(left=dfUniqueClubs, right=dfLeagueKPI, how='left', left_on='club_id', right_on='club_id')
        dfTransClean = dfTrans[['to_club_id', 'to_club_name', 'from_club_id', 'from_club_name']]
        dfTransClean = dfTransClean[(dfTransClean['to_club_id'] != -1) | (dfTransClean['from_club_id'] != -2)]
        dfTransClean.to_csv('transfers.csv', index=False, encoding="iso-8859-15", header=('Target', 'Zile Name','Source', 'Ursprung Name'))
        dfUniqueClubs.to_csv('nodes.csv', index=False, encoding="iso-8859-15", header=('Id', 'Label','Eingehende Trans.', 'Einnahmen'
                                                                                       , 'Ausgehende Trans.', 'Ausgaben', 'AVG Rang',
                                                                                       'Median Rang', 'Cup', 'Liga'))



    def __GetThickness(self, df, row):
        toClub = row["to_club_name"]
        fromClub = row["from_club_name"]
        count = df[df["to_club_name"].str.contains(toClub) & df["from_club_name"].str.contains(fromClub)].shape[0]
        return count

    def GetClubToClubTransferRatio(self, fee, season, clubFilter):
        print("preparing transfer ratio")
        df = self.__cleanLoadTransfers()
        df = self.__filterSeasons(df, fee, season)
        df = df[df["to_club_name"].isin(clubFilter) | (df["from_club_name"].isin(clubFilter))]
        feeIncomeSumByClub = df.groupby(["from_club_name"]).agg({"fee": "sum"})["fee"].to_dict()
        feeExpenseSumByClub = df.groupby(["to_club_name"]).agg({"fee": "sum"})["fee"].to_dict()

        feeRatioByClub = {}
        for clubName in feeIncomeSumByClub:
            income = feeIncomeSumByClub[clubName] if clubName in feeIncomeSumByClub else 0
            expense = feeExpenseSumByClub[clubName] if clubName in feeExpenseSumByClub else 0
            ratio = income - expense
            if ratio < 0:
                ratio = 0
            feeRatioByClub[clubName] = ratio

        df = df[["from_club_name", "to_club_name"]]
        return df, feeRatioByClub

    def GetClubToClubTransferExpense2(self, fee, season, clubFilter):
        print("preparing transfer expenses")
        df = self.__cleanLoadTransfers()
        df = self.__filterSeasons(df, fee, season)
        df = df[df["to_club_name"].isin(clubFilter)]
        transferExpenseByClub = df.groupby(["to_club_name"]).agg({"fee": "sum"})["fee"].to_dict()
        df = df[["from_club_name", "to_club_name"]]
        return df, transferExpenseByClub

    def GetClubToClubTransferIncome(self, fee, season, clubFilter):
        print("preparing transfer income")
        df = self.__cleanLoadTransfers()
        df = self.__filter(df, fee, season)
        df = df[df["from_club_name"].isin(clubFilter)]
        transferIncomeByClub = df.groupby(["from_club_name"]).agg({"fee": "sum"})["fee"].to_dict()
        df = df[["from_club_name", "to_club_name"]]
        return df, transferIncomeByClub

    def GetClubFromNationsToPair(self, fee=1000000, season=None, clubFilter=None):
        df = self.__cleanLoadTransfers()
        df = self.__filter(df, fee, season, clubFilter)
        nationByPlayers = self.__loadPlayersNationality()
        df = df[["from_club_name", "to_club_name", "player_name"]]
        df["nationality"] = df["player_name"].apply(lambda x: nationByPlayers[x])
        df = df[["from_club_name", "nationality"]]

        return df

    def __filterSeasons(self, df, fee, season):
        df = df[df["fee"].notna()]
        df = df.drop(df[df["fee"] <= fee].index)
        df = df[df['from_club_id'].notna()]
        df = df[df['to_club_id'].notna()]

        if season != None:
            seasonFrom = season.split("-")[0]
            seasonTo = season.split("-")[1]
            df = df[df["season"] >= int(seasonFrom)]
            df = df[df["season"] <= int(seasonTo)]
            print("filters season -> df shape: ", df.shape)

        print("shape of dataframe: ", df.shape)

        return df
    def __filterSeasonClubs(self, df, season, league):
        if season != None:
            seasonFrom = season.split("-")[0]
            seasonTo = season.split("-")[1]
            df = df[df["season"] >= int(seasonFrom)]
            df = df[df["season"] <= int(seasonTo)]
            df = df.loc[df['league_id'] == league]
            print("filters season clubs -> df shape: ", df.shape)
        return df

    def __cleanLoadTransfers(self):
        transfers = "./data/transfers.csv"
        df = pd.read_csv(transfers, sep=";", encoding="iso-8859-15")
        print("dataframe loaded. df shape: ", df.shape)
        df["from_club_name"] = df["from_club_name"].apply(lambda x: x.strip())
        df = df.drop(df[df["to_club_name"] == "Unknown"].index)
        df = df.drop(df[df["to_club_name"] == "Retired"].index)
        df.rename(columns=lambda x: x.strip())

        return df

    def __loadPlayersNationality(self):
        players = "./data/dict_players.csv"
        df = pd.read_csv(players, sep=";", encoding="iso-8859-15")
        df = df[["name", "nationality_name"]]
        return df.set_index('name')["nationality_name"].to_dict()
