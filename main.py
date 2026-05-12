import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import networkx as nx

from graph_data import CairoTransportGraph
from shortest_path import RoutePlanner
from mst import MSTOptimizer
from emergency import EmergencySystem
from simulation import TrafficSimulator
from greedy import TrafficSignalGreedy


class SmartCityGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Smart City Transportation System")
        self.root.geometry("1300x750")
        self.root.configure(bg="#e6ecf0")

        self.cairo = CairoTransportGraph()
        self.cairo.load_sample_data()

        self.graph = self.cairo.graph

        self.router = RoutePlanner(self.graph)
        self.mst_solver = MSTOptimizer(self.graph)
        self.emergency = EmergencySystem(self.graph)
        self.simulator = TrafficSimulator(self.graph)
        self.greedy = TrafficSignalGreedy()

        self.create_layout()

        self.draw_graph(self.graph)

    def create_layout(self):

        title = tk.Label(
            self.root,
            text="SMART CITY TRANSPORTATION SYSTEM",
            font=("Arial", 24, "bold"),
            bg="#003366",
            fg="white",
            pady=15
        )

        title.pack(fill="x")

        main_frame = tk.Frame(self.root, bg="#e6ecf0")
        main_frame.pack(fill="both", expand=True)

        # LEFT CONTROL PANEL
        control_panel = tk.Frame(
            main_frame,
            bg="white",
            width=320,
            bd=3,
            relief="ridge"
        )

        control_panel.pack(side="left", fill="y", padx=10, pady=10)

        # GRAPH PANEL
        self.graph_panel = tk.Frame(
            main_frame,
            bg="white",
            bd=3,
            relief="ridge"
        )

        self.graph_panel.pack(
            side="right",
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # CONTROLS
        tk.Label(
            control_panel,
            text="Source Node",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(pady=8)

        self.source_combo = ttk.Combobox(
            control_panel,
            values=list(self.graph.nodes()),
            width=28
        )

        self.source_combo.pack(pady=5)

        tk.Label(
            control_panel,
            text="Destination Node",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(pady=8)

        self.destination_combo = ttk.Combobox(
            control_panel,
            values=list(self.graph.nodes()),
            width=28
        )

        self.destination_combo.pack(pady=5)

        # BUTTONS
        buttons = [

            ("Find Shortest Path",
             self.find_shortest_path,
             "#3498db"),

            ("Emergency Route",
             self.find_emergency_route,
             "#e74c3c"),

            ("Show Minimum Spanning Tree",
             self.show_mst,
             "#2ecc71"),

            ("Rush Hour Simulation",
             self.simulate_rush_hour,
             "#f39c12"),

            ("Traffic Signal Optimization",
             self.optimize_traffic,
             "#9b59b6"),

            ("Reset Network",
             self.reset_network,
             "#34495e")
        ]

        for text, command, color in buttons:

            btn = tk.Button(
                control_panel,
                text=text,
                command=command,
                width=28,
                height=2,
                bg=color,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                cursor="hand2"
            )

            btn.pack(pady=7)

        # RESULTS BOX
        tk.Label(
            control_panel,
            text="Results",
            font=("Arial", 13, "bold"),
            bg="white"
        ).pack(pady=10)

        self.result_box = tk.Text(
            control_panel,
            width=35,
            height=16,
            font=("Consolas", 10),
            bd=2,
            relief="solid"
        )

        self.result_box.pack(pady=5)

    def draw_graph(self, graph, path=None):

        for widget in self.graph_panel.winfo_children():
            widget.destroy()

        figure = plt.Figure(figsize=(9, 7), dpi=100)

        ax = figure.add_subplot(111)

        pos = nx.spring_layout(graph, seed=42)

        nx.draw(
            graph,
            pos,
            ax=ax,
            with_labels=True,
            node_color="skyblue",
            node_size=2500,
            font_size=10,
            font_weight="bold",
            edge_color="gray"
        )

        weights = nx.get_edge_attributes(graph, 'weight')

        nx.draw_networkx_edge_labels(
            graph,
            pos,
            edge_labels=weights,
            ax=ax
        )

        # HIGHLIGHT PATH
        if path:

            path_edges = list(zip(path, path[1:]))

            nx.draw_networkx_edges(
                graph,
                pos,
                edgelist=path_edges,
                edge_color="red",
                width=5,
                ax=ax
            )

        ax.set_title(
            "Transportation Network",
            fontsize=16,
            fontweight="bold"
        )

        canvas = FigureCanvasTkAgg(
            figure,
            master=self.graph_panel
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    def show_result(self, text):

        self.result_box.delete(1.0, tk.END)

        self.result_box.insert(tk.END, text)

    def find_shortest_path(self):

        source = self.source_combo.get()
        destination = self.destination_combo.get()

        try:

            path, distance = self.router.dijkstra_route(
                source,
                destination
            )

            result = (
                "=== DIJKSTRA SHORTEST PATH ===\n\n"
                f"Path:\n{path}\n\n"
                f"Distance: {distance}"
            )

            self.show_result(result)

            self.draw_graph(self.graph, path)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def find_emergency_route(self):

        source = self.source_combo.get()
        destination = self.destination_combo.get()

        try:

            path = self.emergency.emergency_route(
                source,
                destination
            )

            result = (
                "=== EMERGENCY ROUTE ===\n\n"
                f"{path}"
            )

            self.show_result(result)

            self.draw_graph(self.graph, path)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_mst(self):

        mst = self.mst_solver.prim_algorithm()

        cost = self.mst_solver.calculate_cost(mst)

        result = (
            "=== MINIMUM SPANNING TREE ===\n\n"
            f"Total Cost = {cost}"
        )

        self.show_result(result)

        self.draw_graph(mst)

    def simulate_rush_hour(self):

        self.simulator.apply_rush_hour()

        self.show_result(
            "=== RUSH HOUR SIMULATION ===\n\n"
            "Traffic increased on all roads.\n"
            "Edge weights updated successfully."
        )

        self.draw_graph(self.graph)

    def optimize_traffic(self):

        intersections = [
            ("Tahrir", 100),
            ("Ramses", 80),
            ("Dokki", 60),
            ("Maadi", 40)
        ]

        optimized = self.greedy.optimize_signals(
            intersections
        )

        text = "=== TRAFFIC SIGNAL OPTIMIZATION ===\n\n"

        for node, time in optimized:
            text += f"{node} → Green Time: {time}\n"

        self.show_result(text)

    def reset_network(self):

        self.cairo = CairoTransportGraph()
        self.cairo.load_sample_data()

        self.graph = self.cairo.graph

        self.router = RoutePlanner(self.graph)

        self.show_result(
            "=== NETWORK RESET ===\n\n"
            "Graph restored successfully."
        )

        self.draw_graph(self.graph)


root = tk.Tk()

app = SmartCityGUI(root)

root.mainloop()