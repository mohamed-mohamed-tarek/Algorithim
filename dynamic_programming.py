class PublicTransportDP:

    def optimize_buses(self, passengers, buses):
        n = len(passengers)

        dp = [0] * (n + 1)

        for i in range(1, n + 1):
            dp[i] = dp[i - 1] + min(passengers[i - 1], buses)

        return dp[n]


class RoadMaintenanceDP:

    def optimize_maintenance(self, roads, budget):
        n = len(roads)

        dp = [[0 for _ in range(budget + 1)]
              for _ in range(n + 1)]

        for i in range(1, n + 1):
            cost, importance = roads[i - 1]

            for b in range(budget + 1):
                if cost <= b:
                    dp[i][b] = max(dp[i - 1][b],
                                   dp[i - 1][b - cost] + importance)
                else:
                    dp[i][b] = dp[i - 1][b]

        return dp[n][budget]