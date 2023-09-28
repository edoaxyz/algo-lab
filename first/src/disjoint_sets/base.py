"""
Modulo per la gestione base dglie insiemi disgiunti.
"""
from typing import Any


class Node:
    """
    Classe generica per rappresentare un
    elemento in un insieme disgiunto.
    """

    def __init__(self, data: Any):
        self.data: Any = data


class DisjointSetsInterface:
    """
    Interfaccia da implementare per gli insiemi disgiunti.
    """

    def make_set(self, data) -> Node:
        """Crea un nuovo insieme disgiunto."""
        raise NotImplementedError()

    def find_set(self, node: Node) -> Node:
        """Individua il rappresentante dell'insieme."""
        raise NotImplementedError()

    def union(self, node_1: Node, node_2: Node) -> Node:
        """Unisce gli insiemi dei due nodi."""
        raise NotImplementedError()
