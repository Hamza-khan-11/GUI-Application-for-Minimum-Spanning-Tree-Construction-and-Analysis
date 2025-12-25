**GUI Application for Minimum Spanning Tree Construction and Analysis**

Developed as part of the Design and Analysis of Algorithm (CT-363) course, this project is a Python-based graphical user interface (GUI) designed to visualize and analyze the construction of Minimum Spanning Trees (MST). It implements two foundational algorithms: Prim’s and Kruskal’s.

**Features**

Interactive Graph Building: Dynamically add vertices and weighted edges through the GUI.

Dual Algorithm Execution: Run both Prim's and Kruskal's algorithms on the same dataset.

Side-by-Side Visualization: Visual comparison of generated MSTs using Matplotlib and NetworkX.

Data Management: Import and export graph edge lists using CSV files for reproducibility.

Performance Metrics: Displays total MST weight and accuracy comparisons.

Export Results: Save generated MST visualizations as image files for documentation.

**Tools & Technologies**

Language: Python 

GUI Framework: Tkinter 

Graph Processing: NetworkX 

Visualization: Matplotlib 

File Handling: CSV module 

**Algorithm Overview**

The application analyzes two primary approaches to finding an MST:

**Prim’s Algorithm:** Operates by selecting the minimum weight edge from a visited node to an unvisited node, utilizing a priority queue (Min-Heap). It is generally more efficient for dense graphs.

**Kruskal’s Algorithm:** Sorts all edges by weight and adds the smallest edge that does not form a cycle, using a Union-Find data structure. It typically performs better on sparse graphs.

**Installation & Usage**

Clone the repository:

Bash

git clone https://github.com/yourusername/MST-Visualizer.git

Install dependencies:

Bash

pip install matplotlib networkx

Run the application:

Bash

python PROJECT.py

**Limitations & Future Work**

Current limitations include support only for undirected, connected graphs and manual entry for large datasets. Future iterations aim to include:

Support for directed and disconnected graphs.

Step-by-step animations of algorithm progress.

Integration of Boruvka’s algorithm.
