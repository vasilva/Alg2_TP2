import numpy as np
import networkx as nx
from tsp import TSP

adj = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0],
]

G = nx.from_numpy_array(np.array(adj))
N = len(G)
T = TSP(G)
BB_final_res, BB_final_path = T("bb")
TAT_final_res, TAT_final_path = T("tat")
ch_final_res, ch_final_path = T("ch")

print("Branch and Bound")
print(f"Minimum cost: {BB_final_res}")
print(f"Path Taken: {BB_final_path}")

print("-" * 50)

print("Twice Around the Tree")
print(f"Minimum cost: {TAT_final_res}")
print(f"Path Taken: {TAT_final_path}")

print("-" * 50)

print("Christofides")
print(f"Minimum cost: {ch_final_res}")
print(f"Path Taken: {ch_final_path}")
