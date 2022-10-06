"""
Utility functions.
"""
import pandas as pd
import numpy as np
import random
from networkx import Graph
from cnas.types import NODE, EDGE
from typing import List, Any, Dict


def datadict(df: pd.DataFrame, group: str):
    g_list = df[group].unique()
    data = {}
    for g in g_list:
        data[g] = df[df[group]==g]

    return data

def tolist(value: Any) -> List[Any]:
    """
    Convert value or list to list of values.
    If already list, return object directly

    Args:
        value (Any): value to convert
    Returns:
        List[Any]: list of values
    """
    if isinstance(value, (tuple, list)):
        return value
    else:
        return [value]

def list_mean(l: list, axis: int = 0):
    l_np = np.array(l)
    l_avg = np.mean(l_np, axis=axis)

    return l_avg.tolist()

def list_dim(l: list):
    l_np = np.array(l)
    return l_np.ndim

def remove_random_nodes(graph: Graph, num: int):
    for _ in range(num):
        node = random.choice(list(graph.nodes))

        graph.remove_node(node)

def remove_random_egdes(graph: Graph, num: int):
    for _ in range(num):
        edge = random.choice(list(graph.edges))

        graph.remove_edge(*edge)

def remove_targeted_nodes(graph: Graph, nodes: List[NODE]):
    for n in nodes:
        graph.remove_node(n)

def remove_targeted_edges(graph: Graph, edges: List[EDGE]):
    for e in edges:
        graph.remove_edge(*e)

def dict2list(D: Dict[NODE, Dict[NODE, Any]]):
    l = []
    for i in D.values():
        l.append(list(i.values()))

    return l