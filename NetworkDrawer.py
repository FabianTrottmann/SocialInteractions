import networkx as nx
import matplotlib.pyplot as plt

class NetworkDrawer:

    def Draw(self, df, ratioByClub, resizeNodesIndegree, resizeNodesOutdegree):
        # expected high indegree: e.g. paris, inter
        # expected high outdegree: e.g. ajax as an education club
        source = list(df.columns)[0]
        target = list(df.columns)[1]
        clubRelations = nx.from_pandas_edgelist(df, source=source, target=target, create_using=nx.DiGraph())

        n_nodes = clubRelations.number_of_nodes()
        print("number of nodes: ", clubRelations.number_of_nodes())
        sizes = []
        if len(ratioByClub) > 0:
            print("ratio sizes used")
            for nodeName in clubRelations.nodes()._nodes:
                nodeName = nodeName.strip()
                size = ratioByClub[nodeName] if nodeName in ratioByClub else 0
                sizes.append(size/100000)
        elif resizeNodesIndegree:
            print("size based on indegree")
            degree = nx.in_degree_centrality(clubRelations)  # normalized
            for i in degree: # store actual count of incoming to indegree list instead of normalized value
                degree[i] = int(degree[i] * (n_nodes - 1))  # we get nice integeres - the number of incoming ties
            sizes = [v ** 3 + 50 for v in degree.values()]
        elif resizeNodesOutdegree:
            print("size based on outdegree")
            degree = nx.out_degree_centrality(clubRelations)  # normalized
            for i in degree: # store actual count of incoming to indegree list instead of normalized value
                degree[i] = int(degree[i] * (n_nodes - 1))  # we get nice integeres - the number of incoming ties
            sizes = [v ** 2 + 50 for v in degree.values()]

        if len(sizes) > 0:
            coords = nx.kamada_kawai_layout(clubRelations)
            #nx.draw(clubRelations, with_labels=True, pos=coords, node_size=sizes)
            nx.draw(clubRelations, with_labels=True, pos=coords, node_size=sizes)
        else:
            coords = nx.kamada_kawai_layout(clubRelations)
            nx.draw(clubRelations, with_labels=True, pos=coords)

        plt.show()