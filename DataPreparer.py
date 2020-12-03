import pandas as pd


class DataPreparer:

    def GetClubFromClubToPair(self, fee=1000000, season=None, clubsFrom=None):
        df = self.__cleanLoadTransfers()
        df = self.__filter(df, fee, season, clubsFrom)
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

        print("clubs -> clubs. shape of dataframe: ", df.shape)
        return df, feeRatioByClub

    def GetClubFromNationsToPair(self, fee=1000000, season=None, clubsFrom=None):
        df = self.__cleanLoadTransfers()
        df = self.__filter(df, fee, season, clubsFrom)
        nationByPlayers = self.__loadPlayersNationality()
        df = df[["from_club_name", "to_club_name", "player_name"]]
        df["nationality"] = df["player_name"].apply(lambda x: nationByPlayers[x])
        df = df[["from_club_name", "nationality"]]

        print("clubs -> nations. shape of dataframe: ", df.shape)
        return df

    def __filter(self, df, fee, season, clubsFrom):
        df = df[df["fee"].notna()]
        df = df.drop(df[df["fee"] < fee].index)

        if season != None:
            seasonFrom = season.split("-")[0]
            seasonTo = season.split("-")[1]
            df = df[df["season"] >= int(seasonFrom)]
            df = df[df["season"] <= int(seasonTo)]
            print("filters season -> df shape: ", df.shape)
            print(df["season"])
        if clubsFrom != None and len(clubsFrom) > 0:
            df = df[df["from_club_name"].isin(clubsFrom)]
            print("filters from_clubs_name. df shape: ", df.shape)
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
