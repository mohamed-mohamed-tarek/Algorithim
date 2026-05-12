import networkx as nx

class RoutePlanner:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra_route(self, source, destination):
        path = nx.dijkstra_path(self.graph,
                                source,
                                destination,
                                weight='weight')

        distance = nx.dijkstra_path_length(self.graph,
                                           source,
                                           destination,
                                           weight='weight')

        return path, distance

    def astar_route(self, source, destination):
        path = nx.astar_path(self.graph,
                             source,
                             destination,
                             heuristic=lambda u, v: 1,
                             weight='weight')

        return path