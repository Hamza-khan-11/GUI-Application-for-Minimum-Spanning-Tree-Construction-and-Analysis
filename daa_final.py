import tkinter as tk
from tkinter import messagebox
import heapq

class PrimMSTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimum Spanning Tree (Prim's Algorithm)")
        self.root.geometry("450x350")
        self.root.configure(bg="#2C3E50")

        # Variables
        self.num_vertices = tk.IntVar()
        self.edges = []
        
        tk.Label(root, text="Number of Vertices:", fg="white", bg="#2C3E50").pack()
        self.vertex_entry = tk.Entry(root, textvariable=self.num_vertices)
        self.vertex_entry.pack()

        tk.Label(root, text="Enter Edge (u v weight):", fg="white", bg="#2C3E50").pack()
        self.edge_entry = tk.Entry(root)
        self.edge_entry.pack()

        tk.Button(root, text="Add Edge", command=self.add_edge, bg="#27AE60", fg="white").pack(pady=5)
        tk.Button(root, text="Compute MST", command=self.compute_mst, bg="#E74C3C", fg="white").pack(pady=5)

        self.result_label = tk.Label(root, text="MST will be displayed here", fg="white", bg="#2C3E50", font=("Helvetica", 12), justify="left")

        self.result_label.pack(pady=10)

    def add_edge(self):
        edge_text = self.edge_entry.get()
        try:
            u, v, w = map(int, edge_text.split())
            self.edges.append((w, u, v))  # Storing edges as (weight, u, v) for Prim's
            self.edge_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Enter values in format: u v weight")

    def compute_mst(self):
        n = self.num_vertices.get()
        if n <= 0:
            messagebox.showerror("Error", "Enter a valid number of vertices")
            return

        if not self.edges:
            messagebox.showerror("Error", "Add at least one edge")
            return

        # Build adjacency list
        graph = {i: [] for i in range(n)}
        for w, u, v in self.edges:
            graph[u].append((w, v))
            graph[v].append((w, u))

               # Run Prim's Algorithm
        _, prim_weight = self.prim_mst(n, graph)

        # Run Kruskal's Algorithm
        kruskal_weight = self.kruskal_mst(n, self.edges)

        if prim_weight is None or kruskal_weight is None:
            messagebox.showerror("Error", "Graph must be connected!")
            return
        
        prim_acc, kruskal_acc = self.calculate_individual_accuracies(prim_weight, kruskal_weight)


        result_text = (
            f"Total Weight using Prim's Algorithm: {prim_weight}\n"
            f"Total Weight using Kruskal's Algorithm: {kruskal_weight}\n\n"
            f"Accuracy of Prim's Algorithm: {prim_acc}%\n"
            f"Accuracy of Kruskal's Algorithm: {kruskal_acc}%"
        )

        self.result_label.config(text=result_text)


    def prim_mst(self, n, graph):
        visited = set()
        min_heap = [(0, 0, -1)]  # (weight, current node, previous node)
        mst_edges = []
        total_weight = 0

        while len(visited) < n and min_heap:
            w, u, prev = heapq.heappop(min_heap)
            if u in visited:
                continue
            visited.add(u)
            if prev != -1:
                mst_edges.append((prev, u, w))
                total_weight += w
            for weight, v in graph[u]:
                if v not in visited:
                    heapq.heappush(min_heap, (weight, v, u))

        return (mst_edges, total_weight) if len(mst_edges) == n - 1 else (None, None)
    
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
        
        edges_sorted = sorted(edges)
        total_weight = 0
        count = 0

        for w, u, v in edges_sorted:
            if union(u, v):
                total_weight += w
                count += 1
                if count == n - 1:
                    break

        return total_weight if count == n - 1 else None
        
    def calculate_individual_accuracies(self, prim_weight, kruskal_weight):
        optimal_weight = min(prim_weight, kruskal_weight)
        prim_accuracy = round((optimal_weight / prim_weight) * 100, 2) if prim_weight else 0.0
        kruskal_accuracy = round((optimal_weight / kruskal_weight) * 100, 2) if kruskal_weight else 0.0
        return prim_accuracy, kruskal_accuracy





if __name__ == "__main__":
    root = tk.Tk()
    app = PrimMSTApp(root)
    root.mainloop()