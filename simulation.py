class TrafficSimulator:
    def __init__(self, graph):
        self.graph = graph

    def apply_rush_hour(self):
        for u, v, data in self.graph.edges(data=True):
            data['weight'] += 10

    def apply_normal_traffic(self):
        for u, v, data in self.graph.edges(data=True):
            data['weight'] = data['distance'] + data['traffic']