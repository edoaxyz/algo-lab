from graphs import Graph
from disjoint_sets import ListDisjointSets, HeuristicDisjointSets, ForestDisjointSets

g = Graph(5)
g.add_connection(1, 4)
g.add_connection(4, 2)

print(g.get_connected_components(ForestDisjointSets))