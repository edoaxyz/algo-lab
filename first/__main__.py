import time
import numpy as np
import matplotlib.pyplot as plt

from disjoint_sets import ListDisjointSets, ForestDisjointSets, HeuristicDisjointSets
from graphs import Graph

print("Generating graphs...")
graphs = [
    Graph.random_generate_with_coverage(n_vertices, coverage)
    for coverage in np.linspace(0.1, 1, 5)
    for n_vertices in range(100, 1000, 100) #np.logspace(1, 12, 50, base=4, dtype=int)
]
uf_implementations = [ListDisjointSets, HeuristicDisjointSets, ForestDisjointSets]

results = {}

print("Calculating times...")
for graph in graphs:
    results[graph] = {}
    for uf_impl in uf_implementations:
        start = time.time()
        graph.get_connected_components(uf_impl)
        end = time.time()
        results[graph][uf_impl] = end - start

print(results)
