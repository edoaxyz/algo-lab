"""
Modulo per la gestione dei grafi non diretti (non orientati).
"""
import random
import numpy as np
from itertools import combinations
from typing import Any, Type, Self

from disjoint_sets import DisjointSetsInterface


class Vertex:
    """
    Vertice di un grafo.
    """

    def __init__(self, index: int, data: Any = None):
        self.data: Any = data
        self._index: int = index

    def get_index(self) -> int:
        """
        Indice del vertice.
        """
        return self._index


class Graph:
    """
    Grafo non diretto con gestione dei vertici tramite indici.
    """

    def __init__(self, n_vertices: int):
        self._vertices: list[Vertex] = []
        for i in range(n_vertices):
            self._vertices.append(Vertex(i))
        self._connections: set[tuple[Vertex, Vertex]] = set()

    def add_connection(self, start: int, end: int):
        """
        Aggiunge una nuova connessione non diretta tra due nodi.
        """
        if start != end:
            if start > end:
                start, end = end, start
            self._connections.add(tuple([self._vertices[start], self._vertices[end]]))

    def get_connected_components(
        self, union_find_cls: Type[DisjointSetsInterface]
    ) -> list[list[int]]:
        """
        Esegue l'algoritmo per individuare le componenti connesse
        nel grafo.
        """
        union_find_data = union_find_cls()
        for vertex in self._vertices:
            vertex.data = union_find_data.make_set(vertex)
        for conn in self._connections:
            first_node, second_node = union_find_data.find_set(
                conn[0].data
            ), union_find_data.find_set(conn[1].data)
            if first_node != second_node:
                union_find_data.union(first_node, second_node)
        connected_components = {}
        for vertex in self._vertices:
            root = union_find_data.find_set(vertex.data)
            if root not in connected_components:
                connected_components[root] = []
            connected_components[root].append(vertex.get_index())
        return list(connected_components.values())

    def get_vertices_size(self) -> int:
        """
        Ritorna il numero di vertici.
        """
        return len(self._vertices)

    def get_connections_size(self) -> int:
        """
        Ritorna il numero di archi.
        """
        return len(self._connections)

    def get_connection_coverage(self) -> float:
        """
        Ritorna la percentuale di archi presenti rispetto
        al loro numero massimo.
        """
        max_connections = self.get_vertices_size() * (self.get_vertices_size() - 1) / 2
        return self.get_connections_size() / max_connections

    @classmethod
    def random_generate(
        cls: Type[Self], n_vertices: int, n_connections: int = None
    ) -> Self:
        """
        Genera un grafo partendo dal numero di vertici e, opzionalmente,
        dal numero di archi. Gli archi vengono impostati casualmente.
        Se non fornito, anche il numero di archi è generato casualmente
        tra 1 e il numero massimo di archi ammissibile in un grafo non
        diretto i.e. [n*(n-1)]/2 con n il numero di vertici.
        """
        graph = cls(n_vertices)
        max_connections = n_vertices * (n_vertices - 1) / 2
        if n_connections is None:
            n_connections = random.randint(1, max_connections)
        n_connections = max(max_connections, n_connections)
        for sample in np.random.default_rng().choice(
            np.fromiter(combinations(range(n_vertices), 2), tuple), int(n_connections)
        ):
            graph.add_connection(*sample)
        return graph

    @classmethod
    def random_generate_with_coverage(
        cls: Type[Self], n_vertices: int, connections_coverage: float
    ) -> Self:
        """
        Genera un grafo utilizzando la funzione generate_random_graph,
        con il parametro obbligatorio connections_coverage che ammette valori
        tra 0 e 1 che stabilisce il numero di archi (0 -> nessun arco,
        1 -> tutti i nodi sono collegati tra loro)
        """
        connections_coverage = max(min(connections_coverage, 1), 0)

        return cls.random_generate(
            n_vertices, int(n_vertices * (n_vertices - 1) / 2 * connections_coverage)
        )
