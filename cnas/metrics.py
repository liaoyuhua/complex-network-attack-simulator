"""
Supplementary metrics.
"""
import networkx as nx
from networkx import average_shortest_path_length as aspl
from networkx import average_clustering as ac


def directed_global_efficiency(graph: nx.Graph):
    n = len(graph)
    denom = n * (n - 1)
    if denom != 0:
        lengths = nx.all_pairs_shortest_path_length(graph)
        g_eff = 0
        for source, targets in lengths:
            for target, distance in targets.items():
                if distance > 0:
                    g_eff += 1 / distance
        g_eff /= denom
        # g_eff = sum(1 / d for s, tgts in lengths
        #                   for t, d in tgts.items() if d > 0) / denom
    else:
        g_eff = 0
    # TODO This can be made more efficient by computing all pairs shortest
    # path lengths in parallel.
    return g_eff


class average_shortest_path_length:
    def __init__(
        self,
        weight=None, 
        method=None
    ) -> None:
        self.weight = weight
        self.method = method

    def __call__(self, G):
        return aspl(G, weight=self.weight, method=self.method)

class average_clustering:
    def __init__(
        self,
        nodes=None,
        weight=None,
        count_zeros=True
    ) -> None:
        self.nodes = nodes
        self.weight = weight
        self.count_zeros = count_zeros

    def __call__(self, G):
        return ac(G, nodes=self.nodes, weight=self.weight, count_zeros=self.count_zeros)