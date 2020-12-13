import networkx as nx
import matplotlib.pyplot as plt
import pathpy as pp
from pathpy.classes.network import network_from_networkx

class NetworkDrawer:
    def Draw(self, df, transferByClub):
        source = list(df.columns)[0]
        target = list(df.columns)[1]
        clubRelations = nx.from_pandas_edgelist(df, source=source, target=target, create_using=nx.DiGraph())

        n_nodes = clubRelations.number_of_nodes()
        print("number of nodes: ", n_nodes)
        print(df[df["to_club_name"] == "Paris SG"])
        sizes = []
        nodeColor = []
        keyExpense = ''
        keyIncome = ''
        for nodeName in clubRelations.nodes()._nodes:
            if "Income" in nodeName:
                nodeColor.append("red")
                keyIncome = nodeName
            elif "Expense" in nodeName:
                nodeColor.append("red")
                keyExpense = nodeName
            else:
                nodeColor.append("blue")
            nodeName = nodeName.strip()
            size = transferByClub[nodeName] if nodeName in transferByClub else 0
            sizes.append(size/100000) # divide by experimental value which provides nice node size representation

        coords = nx.kamada_kawai_layout(clubRelations)
        coords[keyIncome] = [2, 0.6]
        coords[keyExpense] = [2, -0.6]
        print(coords)

        #fig, ax = plt.subplots(figsize=(12, 5))

        #nx.draw_networkx_nodes(clubRelations,  pos=coords, ax=ax, label=True)#node_size=sizes,
        #nx.draw_networkx_edges(clubRelations, pos=coords, ax=ax) #width=durations,
        #_ = nx.draw_networkx_labels(clubRelations, coords, labels, ax=ax)

        #nx.draw_networkx_nodes(clubRelations, pos=coords, node_size=sizes)
        #nx.draw_networkx_edges(clubRelations, pos=coords, width=durations)

        nx.draw(clubRelations, node_color=nodeColor, with_labels=True, pos=coords, node_size=sizes)
        #nx.write_gexf(clubRelations, "test.gexf")

        edges = clubRelations.edges
        dict = {}
        for edge in edges:
            fromClub = edge[0]
            toClub = edge[1]
            count = df[df["to_club_name"].str.contains(toClub) & df["from_club_name"].str.contains(fromClub)].shape[0]
            if count != 1:
                dict.update({edge: count})

        # todo: to be able to compare, transfer sum in relation to number of transfer
        # todo: colors of only one edges to grey
        nx.draw_networkx_edge_labels(clubRelations, coords, edge_labels=dict, font_size=8, font_color='red')

        plt.show()


        if False:
            widths = nx.get_edge_attributes(clubRelations, edgeAttr)
            nodelist = clubRelations.nodes()

            plt.figure(figsize=(12, 8))

            pos = nx.shell_layout(clubRelations)
            nx.draw_networkx_nodes(clubRelations, coords,
                                   nodelist=nodelist,
                                   node_size=sizes,
                                   node_color='black',
                                   alpha=0.7)
            nx.draw_networkx_edges(clubRelations, coords,
                                   edgelist=widths.keys(),
                                   width=list(widths.values()),
                                   edge_color='black',
                                   alpha=0.6)
            nx.draw_networkx_labels(clubRelations, pos=coords,
                                    labels=dict(zip(nodelist, nodelist)),
                                    font_color='white')
            plt.show()