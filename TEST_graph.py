import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  # For undirected graph

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def prims_algorithm(self):
        in_mst = [False] * self.size
        key_values = [float('inf')] * self.size
        parents = [-1] * self.size

        key_values[0] = 0  # Start from vertex 0

        for _ in range(self.size):
            u = min((v for v in range(self.size) if not in_mst[v]), key=lambda v: key_values[v])
            in_mst[u] = True

            for v in range(self.size):
                if 0 < self.adj_matrix[u][v] < key_values[v] and not in_mst[v]:
                    key_values[v] = self.adj_matrix[u][v]
                    parents[v] = u

        mst_edges = []
        for v in range(1, self.size):
            if parents[v] != -1:
                mst_edges.append((parents[v], v, self.adj_matrix[v][parents[v]]))
        return mst_edges

# Create Graph and Add Data
g = Graph(5)  # Create a graph with 5 vertices (A, B, C, D, E)
g.add_vertex_data(0, 'A')
g.add_vertex_data(1, 'B')
g.add_vertex_data(2, 'C')
g.add_vertex_data(3, 'D')
g.add_vertex_data(4, 'E')

g.add_edge(0, 1, 2)  # A - B
g.add_edge(0, 2, 3)  # A - c
g.add_edge(1, 2, 1)  # B - C
g.add_edge(1, 3, 4)  # B - D
g.add_edge(2, 3, 5)  # C - D
g.add_edge(3, 4, 6)  # D - E


class MSTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prim's Algorithm MST Visualizer")

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.show_original_btn = tk.Button(self.frame, text="Show Original Graph", command=self.show_original_graph)
        self.show_original_btn.grid(row=0, column=0, padx=10, pady=10)

        self.show_mst_btn = tk.Button(self.frame, text="Show MST Graph", command=self.show_mst_graph)
        self.show_mst_btn.grid(row=0, column=1, padx=10, pady=10)

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

        self.figure = plt.Figure(figsize=(6,6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack()

    def draw_graph(self, edges, title):
        self.ax.clear()

        G = nx.Graph()

        # Add edges
        for u, v, w in edges:
            G.add_edge(g.vertex_data[u], g.vertex_data[v], weight=w)

        pos = nx.spring_layout(G)

        nx.draw(G, pos, with_labels=True, ax=self.ax, node_color='lightblue', edge_color='gray', node_size=600, font_size=10)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax)

        self.ax.set_title(title)
        self.canvas.draw()

    def show_original_graph(self):
        edges = []
        for u in range(g.size):
            for v in range(u, g.size):
                if g.adj_matrix[u][v] != 0:
                    edges.append((u, v, g.adj_matrix[u][v]))
        self.draw_graph(edges, "Original Graph")

    def show_mst_graph(self):
        mst_edges = g.prims_algorithm()
        self.draw_graph(mst_edges, "Minimum Spanning Tree (MST)")

if __name__ == "__main__":
    root = tk.Tk()
    app = MSTApp(root)
    root.mainloop()
