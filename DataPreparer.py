import pandas as pd


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
        #df.to_csv("C:\\Projects\\Python\\SocialInteractions\\data\my.csv", sep=";")
        return df, transferExpenseByClub

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

        if season != None:
            seasonFrom = season.split("-")[0]
            seasonTo = season.split("-")[1]
            df = df[df["season"] >= int(seasonFrom)]
            df = df[df["season"] <= int(seasonTo)]
            print("filters season -> df shape: ", df.shape)

        print("shape of dataframe: ", df.shape)

        return df

    def __cleanLoadTransfers(self):
        transfers = "./data/transfers.csv"
        df = pd.read_csv(transfers, sep=";", encoding="iso-8859-15")
        print("dataframe loaded. df shape: ", df.shape)
        df["from_club_name"] = df["from_club_name"].apply(lambda x: x.strip())
        df = df.drop(df[df["to_club_name"] == "Unknown"].index)
        df = df.drop(df[df["to_club_name"] == "Retired"].index)

        return df

    def __loadPlayersNationality(self):
        players = "./data/dict_players.csv"
        df = pd.read_csv(players, sep=";", encoding="iso-8859-15")
        df = df[["name", "nationality_name"]]
        return df.set_index('name')["nationality_name"].to_dict()
