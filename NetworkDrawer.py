import networkx as nx
import matplotlib.pyplot as plt

class NetworkDrawer:
    def Draw(self, df, clubToCompare, transferByClub):
        source = list(df.columns)[0]
        target = list(df.columns)[1]
        clubRelations = nx.from_pandas_edgelist(df, source=source, target=target, create_using=nx.DiGraph())
        n_nodes = clubRelations.number_of_nodes()
        print("number of nodes: ", n_nodes)

        sizes = []
        nodeColor = []
        for nodeName in clubRelations.nodes()._nodes:
            if nodeName in clubToCompare:
                nodeColor.append("red")
            else:
                nodeColor.append("blue")
            nodeName = nodeName.strip()
            size = transferByClub[nodeName] if nodeName in transferByClub else 0
            sizes.append(size/100000) # divide by experimental value which provides nice node size representation

        coords = nx.kamada_kawai_layout(clubRelations)
        # nx.draw(self.__clubRelations, with_labels=True, pos=coords, node_size=sizes)
        # coords = nx.spring_layout(self.__clubRelations)
        nx.draw(clubRelations, node_color=nodeColor, with_labels=True, pos=coords, node_size=sizes)
        plt.show()