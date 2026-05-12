import networkx as nx

class MSTOptimizer:
    def __init__(self, graph):
        self.graph = graph

    def prim_algorithm(self):
        mst = nx.minimum_spanning_tree(self.graph, algorithm='prim')
        return mst

    def kruskal_algorithm(self):
        mst = nx.minimum_spanning_tree(self.graph, algorithm='kruskal')
        return mst

    def calculate_cost(self, mst):
        total_cost = 0

        for u, v, data in mst.edges(data=True):
            total_cost += data['weight']

        return total_cost