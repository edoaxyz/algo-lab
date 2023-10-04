"""
Modulo per gli insiemi disgiunti gestiti tramite foreste.
"""
from typing import Any

from .base import DisjointSetsInterface, Node


class TreeNode(Node):
    """
    Classe per la gestione di un nodo su alberi.
    """

    def __init__(self, data: Any):
        super().__init__(data)
        self.parent = None


class ForestDisjointSets(DisjointSetsInterface):
    """
    Classe per la gestione di insiemi disgiunti tramite foreste.
    Implementa la compressione dei cammini.
    """

    def make_set(self, data: Any) -> TreeNode:
        return TreeNode(data)

    def find_set(self, node: TreeNode) -> TreeNode:
        if node.parent is None:
            return node
        node.parent = self.find_set(node.parent)
        return node.parent

    def union(self, node_1: TreeNode, node_2: TreeNode) -> TreeNode:
        set_1, set_2 = node_1, self.find_set(node_2)
        set_2.parent = set_1
        return set_1
