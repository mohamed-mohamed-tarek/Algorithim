import matplotlib

# Fix matplotlib backend issue
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import networkx as nx


class GraphVisualizer:

    def draw_graph(self, graph, title="Cairo Transportation Network"):

        plt.figure(figsize=(10, 7))

        pos = nx.spring_layout(graph)

        weights = nx.get_edge_attributes(graph, 'weight')

        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_color='lightblue',
            node_size=2500,
            font_size=10
        )

        nx.draw_networkx_edge_labels(
            graph,
            pos,
            edge_labels=weights
        )

        plt.title(title)

        # Save image instead of opening window
        plt.savefig(f"{title}.png")

        print(f"{title} graph saved successfully.")