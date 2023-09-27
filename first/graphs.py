"""
Modulo per la gestione dei grafi non diretti (non orientati).
"""
import random
from typing import Any, Type, Self

from disjoint_sets import DisjointSetsInterface


class Vertex:
    """
    Vertice di un grafo.
    """

    def __init__(self, index: int, data: Any = None):
        self.data: Any = data
        self._index: int = index

    @property
    def index(self):
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
            first_node, second_node = conn[0].data, conn[1].data
            if union_find_data.find_set(first_node) != union_find_data.find_set(
                second_node
            ):
                union_find_data.union(first_node, second_node)
        connected_components = {}
        for vertex in self._vertices:
            root = union_find_data.find_set(vertex.data)
            if root not in connected_components:
                connected_components[root] = []
            connected_components[root].append(vertex.index)
        return list(connected_components.values())

    @classmethod
    def random_generate(cls: Type[Self], n_vertices: int, n_edges: int = None) -> Self:
        """
        Genera un grafo partendo dal numero di vertici e, opzionalmente,
        dal numero di archi. Gli archi vengono impostati casualmente.
        Se non fornito, anche il numero di archi è generato casualmente
        tra 1 e il numero massimo di archi ammissibile in un grafo non
        diretto i.e. [n*(n-1)]/2 con n il numero di vertici.
        """
        graph = cls(n_vertices)
        max_edges = n_vertices * (n_vertices - 1) / 2
        if n_edges is None:
            n_edges = random.randint(1, max_edges)
        n_edges = max(max_edges, n_edges)
        samples = random.sample(
            [[j, i] for i in range(n_vertices) for j in range(i)], int(n_edges)
        )
        for sample in samples:
            graph.add_connection(*sample)
        return graph

    @classmethod
    def random_generate_with_coverage(
        cls: Type[Self], n_vertices: int, edges_coverage: float
    ) -> Self:
        """
        Genera un grafo utilizzando la funzione generate_random_graph,
        con il parametro obbligatorio edges_coverage che ammette valori
        tra 0 e 1 che stabilisce il numero di archi (0 -> nessun arco,
        1 -> tutti i nodi sono collegati tra loro)
        """
        edges_coverage = max(min(edges_coverage, 1), 0)

        return cls.random_generate(
            n_vertices, n_vertices * (n_vertices - 1) / 2 * edges_coverage
        )
