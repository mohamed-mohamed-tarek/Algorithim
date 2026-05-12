class TrafficSignalGreedy:

    def optimize_signals(self, intersections):
        intersections.sort(key=lambda x: x[1], reverse=True)

        optimized = []

        for name, cars in intersections:
            green_time = cars * 2
            optimized.append((name, green_time))

        return optimized


class EmergencyPriority:

    def prioritize_emergency(self, roads):
        roads.sort(key=lambda x: x[1])
        return roads