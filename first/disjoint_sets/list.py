"""
Modulo per gli insiemi disgiunti gestiti tramite liste concatenate.
"""

from typing import Self, Any

from .base import DisjointSetsInterface, Node


class ListNode(Node):
    """
    Classe per la gestione di un nodo su liste concatenate.
    """

    def __init__(self, data: Any):
        super().__init__(data)
        self.list: "List" = None
        self.next: Self = None


class List:
    """
    Classe rappresentante una lista concatenata.
    """

    def __init__(self):
        self.first: ListNode = None
        self.last: ListNode = None
        self._size = 0

    def add(self, node: ListNode):
        """
        Aggiunge un nodo alla lista.
        """
        node.list = self
        if self.last:
            self.last.next = node
        self.last = node
        if not self.first:
            self.first = node
        self._size += 1

    def __iter__(self):
        """
        Restituisce un iteratore della lista.
        """
        node = self.first
        while node.next is not None:
            yield node
            node = node.next

    @property
    def size(self) -> int:
        """
        Dimensione della lista.
        """
        return self._size

    def merge(self, source_list: Self):
        """
        Inserisce i nodi da una lista data.
        """
        for node in source_list:
            self.add(node)


class ListDisjointSets(DisjointSetsInterface):
    """
    Implementazione di insiemi disgiunti tramite liste concatenate.
    """

    def find_set(self, node: ListNode) -> ListNode:
        return node.list.first

    def make_set(self, data: Any) -> ListNode:
        new_node = ListNode(data)
        new_list = List()
        new_list.add(new_node)
        return new_node

    def union(self, node_1: ListNode, node_2: ListNode) -> ListNode:
        node_1.list.merge(node_2.list)
        return node_1


class HeuristicDisjointSets(ListDisjointSets):
    """
    Implementazione di insiemi disgiunti tramite liste concatenate
    con euristica dell'unione pesata.
    """

    def union(self, node_1: ListNode, node_2: ListNode) -> ListNode:
        if node_1.list.size > node_2.list.size:
            node_1.list.merge(node_2.list)
            return node_1
        node_2.list.merge(node_1.list)
        return node_2
