import time
import csv
import signal
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from disjoint_sets import ListDisjointSets, ForestDisjointSets, HeuristicDisjointSets
from graphs import Graph

signal.signal(signal.SIGINT, signal.SIG_DFL)

COVERAGES = {"lin": [0.75, 1], "poly": [0.75, 1]}
RANGES = {"lin": range(1000, 5100, 1000), "poly": range(100, 1100, 100)}
UF_IMPLEMENTATIONS = {
    "LC": ListDisjointSets,
    "LC/EUP": HeuristicDisjointSets,
    "FCC": ForestDisjointSets,
}
ROUNDS = 3

print("Generating graphs...")
graphs = {
    (
        (
            cov_type,
            coverage,
        ),
        n_vertices,
    ): Graph.random_generate_with_poly_coverage(n_vertices, coverage)
    if cov_type == "poly"
    else Graph.random_generate_with_lin_coverage(n_vertices, coverage)
    for cov_type, coverages in COVERAGES.items()
    for coverage in coverages
    for n_vertices in RANGES[cov_type]
}

results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

print("Calculating times...")
for r in range(ROUNDS):
    print(f"Round {r + 1}...")
    for uf_impl in UF_IMPLEMENTATIONS.values():
        for (cov, vert), graph in graphs.items():
            start = time.time()
            graph.get_connected_components(uf_impl)
            end = time.time()
            results[cov][uf_impl][vert][r] = end - start

print("Calculating medians...")
for uf_impl in UF_IMPLEMENTATIONS.values():
    for cov, vert in graphs.keys():
        values = results[cov][uf_impl][vert]
        values["median"] = np.median([time for time in values.values()])

print("Saving results...")
with open("results.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(
        csvfile,
    )

    writer.writerow(
        [
            "Tipo copertura",
            "Valore copertura",
            "Tipo Union Find",
            "Numero vertici",
            "Tentativo n.",
            "Tempo",
            "Mediana",
        ]
    )
    writer.writerows(
        (
            cov[0],
            cov[1],
            uf_label,
            verts,
            r + 1,
            round(results[cov][uf_impl][verts][r], 3),
            round(results[cov][uf_impl][verts]["median"], 3),
        )
        for cov in results
        for uf_label, uf_impl in UF_IMPLEMENTATIONS.items()
        for verts in results[cov][uf_impl]
        for r in results[cov][uf_impl][verts]
        if r in range(ROUNDS)
    )

print("Showing results...")
for cov in results:
    for label, uf_impl in UF_IMPLEMENTATIONS.items():
        plt.plot(
            results[cov][uf_impl].keys(),
            [values["median"] for values in results[cov][uf_impl].values()],
            label=label,
        )
    plt.title(f"Copertura {cov[0]} {cov[1]*100:.1f}%")
    plt.legend(loc="best")
    plt.xlabel("Vertici")
    plt.ylabel("Tempo (s)")
    plt.show()
