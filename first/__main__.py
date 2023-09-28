import time
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
    for coverage in np.linspace(0.01, 1, 3)#np.logspace(-8, 0, 5, base=2)
    for n_vertices in range(100, 1000, 100)  # np.logspace(1, 12, 50, base=4, dtype=int)
}
UF_IMPLEMENTATIONS = {
    "Liste concatenate": ListDisjointSets,
    "Liste concatenate con euristica dell'unione pesata": HeuristicDisjointSets,
    "Foreste con compressione dei cammini": ForestDisjointSets,
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
            results[uf_impl][cov][vert][round] = end - start

fig, axs = plt.subplots(3)
fig.tight_layout()
for i, (plot_name, uf_impl) in enumerate(UF_IMPLEMENTATIONS.items()):
    axs[i].set_title(plot_name)
    axs[i].set_xlabel("Nodi")
    axs[i].set_ylabel("Tempo")
    for cov, vertices in results[uf_impl].items():
        axs[i].plot(
            vertices.keys(),
            [np.mean(list(times.values())) for times in vertices.values()],
            label=f"{cov * 100:.2f}%",
        )

plt.legend(loc="best")
plt.show()
