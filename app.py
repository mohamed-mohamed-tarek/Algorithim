import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np

from sklearn.linear_model import LinearRegression

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Smart City Transportation System",
    layout="wide"
)

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.title("🚦 Smart City Transportation Network Optimization")

st.markdown(
    """
    This web application demonstrates:

    - Dijkstra Shortest Path
    - A* Emergency Routing
    - Minimum Spanning Tree
    - Rush Hour Simulation
    - Traffic Signal Optimization
    - Dynamic Programming
    - Machine Learning Traffic Prediction
    """
)

# ------------------------------------------------
# GRAPH CREATION
# ------------------------------------------------

G = nx.Graph()

roads = [

    ("Nasr City", "Maadi", 10),

    ("Maadi", "Dokki", 7),

    ("Nasr City", "6th October", 20),

    ("Dokki", "Heliopolis", 8),

    ("Heliopolis", "Maadi", 12),

    ("6th October", "Dokki", 15)
]

for source, destination, weight in roads:

    G.add_edge(
        source,
        destination,
        weight=weight
    )

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.header("System Controls")

source = st.sidebar.selectbox(
    "Select Source",
    list(G.nodes())
)

destination = st.sidebar.selectbox(
    "Select Destination",
    list(G.nodes())
)

algorithm = st.sidebar.selectbox(
    "Choose Algorithm",
    [
        "Dijkstra",
        "A*",
        "Minimum Spanning Tree",
        "Rush Hour Simulation",
        "Traffic Signal Optimization",
        "Dynamic Programming",
        "ML Traffic Prediction"
    ]
)

prediction_hour = st.sidebar.slider(
    "Select Hour",
    0,
    23,
    17
)

run_button = st.sidebar.button("Run Algorithm")

# ------------------------------------------------
# DRAW GRAPH FUNCTION
# ------------------------------------------------

def draw_graph(graph, highlighted_path=None):

    fig, ax = plt.subplots(figsize=(10, 7))

    pos = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=3000,
        font_size=10,
        font_weight="bold",
        edge_color="gray",
        ax=ax
    )

    labels = nx.get_edge_attributes(
        graph,
        'weight'
    )

    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=labels,
        ax=ax
    )

    # Highlight Path
    if highlighted_path:

        edges = list(
            zip(
                highlighted_path,
                highlighted_path[1:]
            )
        )

        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=edges,
            edge_color='red',
            width=5,
            ax=ax
        )

    st.pyplot(fig)

# ------------------------------------------------
# MAIN OPERATIONS
# ------------------------------------------------

if run_button:

    # ------------------------------------------------
    # DIJKSTRA
    # ------------------------------------------------

    if algorithm == "Dijkstra":

        start = time.time()

        path = nx.dijkstra_path(
            G,
            source,
            destination,
            weight='weight'
        )

        distance = nx.dijkstra_path_length(
            G,
            source,
            destination,
            weight='weight'
        )

        end = time.time()

        st.subheader("📍 Dijkstra Shortest Path")

        st.success(
            f"Path: {' → '.join(path)}"
        )

        st.info(
            f"Total Distance = {distance}"
        )

        st.write(
            f"Execution Time: {end - start:.6f} sec"
        )

        draw_graph(G, path)

    # ------------------------------------------------
    # A*
    # ------------------------------------------------

    elif algorithm == "A*":

        start = time.time()

        path = nx.astar_path(
            G,
            source,
            destination,
            heuristic=lambda u, v: 1,
            weight='weight'
        )

        end = time.time()

        st.subheader("🚑 Emergency Route Using A*")

        st.success(
            f"Path: {' → '.join(path)}"
        )

        st.write(
            f"Execution Time: {end - start:.6f} sec"
        )

        draw_graph(G, path)

    # ------------------------------------------------
    # MST
    # ------------------------------------------------

    elif algorithm == "Minimum Spanning Tree":

        mst = nx.minimum_spanning_tree(
            G,
            algorithm='prim'
        )

        total_cost = sum(
            data['weight']
            for _, _, data in mst.edges(data=True)
        )

        st.subheader("🌐 Minimum Spanning Tree")

        st.success(
            f"Total MST Cost = {total_cost}"
        )

        draw_graph(mst)

    # ------------------------------------------------
    # RUSH HOUR
    # ------------------------------------------------

    elif algorithm == "Rush Hour Simulation":

        for u, v, data in G.edges(data=True):
            data['weight'] += 10

        st.subheader("🚗 Rush Hour Traffic Simulation")

        st.warning(
            "Traffic congestion increased on all roads."
        )

        draw_graph(G)

    # ------------------------------------------------
    # GREEDY
    # ------------------------------------------------

    elif algorithm == "Traffic Signal Optimization":

        intersections = [
            ("Tahrir", 100),
            ("Ramses", 80),
            ("Dokki", 60),
            ("Maadi", 40)
        ]

        intersections.sort(
            key=lambda x: x[1],
            reverse=True
        )

        st.subheader("🚦 Traffic Signal Optimization")

        for node, cars in intersections:

            green_time = cars * 2

            st.write(
                f"{node} → Green Time = {green_time} sec"
            )

    # ------------------------------------------------
    # DYNAMIC PROGRAMMING
    # ------------------------------------------------

    elif algorithm == "Dynamic Programming":

        passengers = [100, 200, 150]

        buses = 120

        result = 0

        for p in passengers:
            result += min(p, buses)

        st.subheader(
            "🚌 Public Transportation Scheduling"
        )

        st.success(
            f"Optimized Passenger Coverage = {result}"
        )

    # ------------------------------------------------
    # MACHINE LEARNING
    # ------------------------------------------------

    elif algorithm == "ML Traffic Prediction":

        hours = np.array([
            [6],
            [8],
            [10],
            [12],
            [14],
            [16],
            [18],
            [20]
        ])

        traffic = np.array([
            20,
            80,
            40,
            35,
            50,
            90,
            120,
            60
        ])

        model = LinearRegression()

        model.fit(
            hours,
            traffic
        )

        prediction = model.predict(
            [[prediction_hour]]
        )

        st.subheader(
            "🤖 ML Traffic Prediction"
        )

        st.success(
            f"Predicted Traffic at "
            f"{prediction_hour}:00 = "
            f"{prediction[0]:.2f} Cars"
        )

        fig, ax = plt.subplots()

        ax.plot(
            hours,
            traffic,
            marker='o'
        )

        ax.scatter(
            prediction_hour,
            prediction[0],
            s=200
        )

        ax.set_title(
            "Traffic Prediction"
        )

        ax.set_xlabel(
            "Hour"
        )

        ax.set_ylabel(
            "Traffic Density"
        )

        st.pyplot(fig)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown("---")

st.markdown(
    "### Developed for CSE112 – Design and Analysis of Algorithms"
)