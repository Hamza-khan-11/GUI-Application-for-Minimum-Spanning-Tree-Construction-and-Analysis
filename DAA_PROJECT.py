import tkinter as tk
from tkinter import messagebox, filedialog
import heapq
import matplotlib.pyplot as plt
import networkx as nx
import csv

class MSTVisualizer:
    def __init__(self, root): 
        self.root = root
        self.root.title("MST Visualizer (Prim's & Kruskal's)")
        self.root.geometry("600x600")
        self.root.configure(bg="#2C3E50")

        self.num_vertices = tk.IntVar()
        self.edges = []

        # UI - Labels and Entry
        tk.Label(root, text="Number of Vertices:", fg="white", bg="#2C3E50", font=("Arial", 12)).pack()
        self.vertex_entry = tk.Entry(root, textvariable=self.num_vertices)
        self.vertex_entry.pack(pady=2)

        tk.Label(root, text="Start Vertex:", fg="white", bg="#2C3E50").pack()
        self.u_entry = tk.Entry(root)
        self.u_entry.pack()

        tk.Label(root, text="End Vertex:", fg="white", bg="#2C3E50").pack()
        self.v_entry = tk.Entry(root)
        self.v_entry.pack()

        tk.Label(root, text="Weight:", fg="white", bg="#2C3E50").pack()
        self.w_entry = tk.Entry(root)
        self.w_entry.pack()

        # Listbox to show added edges
        tk.Label(root, text="Edges Added (u, v, w):", fg="white", bg="#2C3E50").pack()
        self.edge_listbox = tk.Listbox(root, height=6, width=40)
        self.edge_listbox.pack(pady=5)

        # Buttons for actions
        tk.Button(root, text="Add Edge", command=self.add_edge, bg="#27AE60", fg="white").pack(pady=5)
        tk.Button(root, text="Compute MST", command=self.compute_mst, bg="#E74C3C", fg="white").pack(pady=5)
        tk.Button(root, text="Import Edges", command=self.import_edges, bg="#F39C12", fg="white").pack(pady=5)
        tk.Button(root, text="Export Edges", command=self.export_edges, bg="#3498DB", fg="white").pack(pady=5)
        tk.Button(root, text="Reset Graph", command=self.reset_graph, bg="#95A5A6", fg="white").pack(pady=5)

        self.result_label = tk.Label(root, text="MST results will appear here", fg="white", bg="#2C3E50", wraplength=500, justify="left")
        self.result_label.pack(pady=10)

    def add_edge(self):
        try:
            u = int(self.u_entry.get())
            v = int(self.v_entry.get())
            w = int(self.w_entry.get())

            if self.num_vertices.get() <= max(u, v):
                raise ValueError("Vertex index exceeds the number of vertices.")

            self.edges.append((w, u, v))
            self.edge_listbox.insert(tk.END, f"({u}, {v}, {w})")

            self.u_entry.delete(0, tk.END)
            self.v_entry.delete(0, tk.END)
            self.w_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers for u, v, and weight within range.")

    def compute_mst(self):
        try:
            n = self.num_vertices.get()
            if n <= 0:
                raise ValueError("Number of vertices must be greater than 0.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        if not self.edges:
            messagebox.showerror("Input Error", "No edges to compute MST.")
            return

        graph = {i: [] for i in range(n)}
        for w, u, v in self.edges:
            graph[u].append((w, v))
            graph[v].append((w, u))

        prim_result, prim_weight = self.prim_mst(n, graph)
        kruskal_weight, kruskal_result = self.kruskal_mst(n, self.edges)

        if prim_weight is None or kruskal_weight is None:
            messagebox.showerror("Disconnected Graph", "Ensure the graph is connected.")
            return

        prim_acc, kruskal_acc = self.calculate_accuracy(prim_weight, kruskal_weight)

        result_text = (
            f"Prim's MST Total Weight: {prim_weight}\n"
            f"Kruskal's MST Total Weight: {kruskal_weight}\n"
            f"\nPrim's Accuracy: {prim_acc}%\n"
            f"Kruskal's Accuracy: {kruskal_acc}%"
        )
        self.result_label.config(text=result_text)
        self.plot_msts(graph, prim_result, kruskal_result)

    def prim_mst(self, n, graph):
        visited = set()
        heap = [(0, 0, -1)]
        mst = []
        total_weight = 0

        while len(visited) < n and heap:
            w, u, prev = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)
            if prev != -1:
                mst.append((prev, u, w))
                total_weight += w
            for weight, v in graph[u]:
                if v not in visited:
                    heapq.heappush(heap, (weight, v, u))

        return (mst, total_weight) if len(mst) == n - 1 else (None, None)

    def kruskal_mst(self, n, edges):
        parent = list(range(n))

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u, v):
            u_root = find(u)
            v_root = find(v)
            if u_root == v_root:
                return False
            parent[v_root] = u_root
            return True

        mst = []
        total_weight = 0
        count = 0

        for w, u, v in sorted(edges):
            if union(u, v):
                mst.append((u, v, w))
                total_weight += w
                count += 1
                if count == n - 1:
                    break

        return total_weight, mst if count == n - 1 else (None, None)

    def calculate_accuracy(self, prim_weight, kruskal_weight):
        best = min(prim_weight, kruskal_weight)
        prim_acc = round((best / prim_weight) * 100, 2)
        kruskal_acc = round((best / kruskal_weight) * 100, 2)
        return prim_acc, kruskal_acc

    def plot_msts(self, graph, prim_mst, kruskal_mst):
        plt.figure(figsize=(12, 6))

        # Prim's MST
        G1 = nx.Graph()
        G1.add_nodes_from(graph.keys())
        G1.add_weighted_edges_from([(u, v, w) for u, v, w in prim_mst])

        pos = nx.spring_layout(G1)
        plt.subplot(121)
        nx.draw(G1, pos, with_labels=True, node_color='lightblue', edge_color='green', node_size=1500, font_size=12)
        nx.draw_networkx_edge_labels(G1, pos, edge_labels={(u, v): w for u, v, w in prim_mst})
        plt.title("Prim's MST")

        # Kruskal's MST
        G2 = nx.Graph()
        G2.add_nodes_from(graph.keys())
        G2.add_weighted_edges_from(kruskal_mst)

        plt.subplot(122)
        nx.draw(G2, pos, with_labels=True, node_color='lightcoral', edge_color='blue', node_size=1500, font_size=12)
        nx.draw_networkx_edge_labels(G2, pos, edge_labels={(u, v): w for u, v, w in kruskal_mst})
        plt.title("Kruskal's MST")

        plt.tight_layout()
        plt.savefig("mst_output.png")
        plt.show()

    def import_edges(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.edges.clear()
            self.edge_listbox.delete(0, tk.END)
            with open(file_path) as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 3:
                        u, v, w = map(int, row)
                        self.edges.append((w, u, v))
                        self.edge_listbox.insert(tk.END, f"({u}, {v}, {w})")
            messagebox.showinfo("Import", "Edges imported successfully!")

    def export_edges(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    for w, u, v in self.edges:
                        writer.writerow([u, v, w])
                messagebox.showinfo("Export", "Edges exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {e}")

    def reset_graph(self):
        self.edges.clear()
        self.edge_listbox.delete(0, tk.END)
        self.result_label.config(text="MST results will appear here")
        messagebox.showinfo("Reset", "Graph has been reset.")

if __name__ == "__main__":  
    root = tk.Tk()
    app = MSTVisualizer(root)
    root.mainloop()
