import time
import csv
import signal
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from disjoint_sets import ListDisjointSets, ForestDisjointSets, HeuristicDisjointSets
from graphs import Graph

signal.signal(signal.SIGINT, signal.SIG_DFL)

print("Generating graphs...")
graphs = {
    (coverage, n_vertices): Graph.random_generate_with_coverage(n_vertices, coverage)
    for coverage in [0.01, 0.5, 1]
    for n_vertices in range(100, 1000, 100)
}
UF_IMPLEMENTATIONS = {
    "LC": ListDisjointSets,
    "LC/EUP": HeuristicDisjointSets,
    "FCC": ForestDisjointSets,
}
ROUNDS = 3

results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

print("Calculating times...")
for round in range(ROUNDS):
    print(f"Round {round + 1}...")
    for uf_impl in UF_IMPLEMENTATIONS.values():
        for (cov, vert), graph in graphs.items():
            start = time.time()
            graph.get_connected_components(uf_impl)
            end = time.time()
            results[cov][uf_impl][vert][round] = end - start

print("Calculating means...")
for uf_impl in UF_IMPLEMENTATIONS.values():
    for cov, vert in graphs.keys():
        values = results[cov][uf_impl][vert]
        values["mean"] = np.mean([time for time in values.values()])

print("Saving results...")
with open("results.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(
        csvfile,
    )

    writer.writerow(
        [
            "Copertura archi",
            "Tipo Union Find",
            "Numero nodi",
            "Tentativo n.",
            "Tempo",
            "Media",
        ]
    )
    writer.writerows(
        (
            cov,
            uf_label,
            verts,
            round + 1,
            results[cov][uf_impl][verts][round],
            results[cov][uf_impl][verts]["mean"],
        )
        for cov in results
        for uf_label, uf_impl in UF_IMPLEMENTATIONS.items()
        for verts in results[cov][uf_impl]
        for round in results[cov][uf_impl][verts]
        if round in range(ROUNDS)
    )

print("Showing results...")
for cov in results:
    for label, uf_impl in UF_IMPLEMENTATIONS.items():
        plt.plot(
            results[cov][uf_impl].keys(),
            [values["mean"] for values in results[cov][uf_impl].values()],
            label=label,
        )
    plt.title(f"Copertura {cov*100:.0f}%")
    plt.legend(loc="best")
    plt.xlabel("Nodi")
    plt.ylabel("Tempo (s)")
    plt.show()
