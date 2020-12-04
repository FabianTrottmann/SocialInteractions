import pandas as pd


class DataPreparer:

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

    def GetClubToClubTransferExpense(self, fee, season, clubFilter):
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
        df = df.drop(df[df["fee"] < fee].index)

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
