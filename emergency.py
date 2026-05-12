from shortest_path import RoutePlanner

class EmergencySystem:
    def __init__(self, graph):
        self.graph = graph
        self.router = RoutePlanner(graph)

    def emergency_route(self, ambulance_location, hospital):
        route = self.router.astar_route(ambulance_location,
                                        hospital)

        return route