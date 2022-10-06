"""
Simulation.
"""
import networkx as nx
import pandas as pd
from copy import deepcopy
from tqdm import tqdm
import math
import matplotlib.pyplot as plt
from typing import Union, List, Optional, Callable
from cnas.utils import (
    datadict,
    tolist,
    list_mean,
    list_dim,
    remove_random_egdes,
    remove_random_nodes,
    remove_targeted_edges,
    remove_targeted_nodes
)


class AttackSimulator:
    """
    TODO Till now, only directed graph is supported.
    TODO Till now, only nodes/edges removal is supported. Perturbation is coming soon.
    """
    def __init__(
        self,
        data: pd.DataFrame,
        head: str,
        tail: str,
        weight: str,
        group_id: str,
        how: str = "node",
        remove: bool = True,
        random: bool = True,
        iter_n: int = 10,
        reverse: bool = True,
        metrics: List[Callable] = None,
    ) -> None:
        """
        Args:
            data (pd.DataFrame):
            head (str):
            tail (str):
            weight (str):
            group_id (str):
            how (str):
            remove (bool):
            random (bool):
            iter_n (int):
            reverse (bool):
            metrics (List[Callable]):
        """
        assert how in ("node", "edge"), f"{how} is not supported"

        self.data = datadict(data, group_id) # this is dict
        self.head = head
        self.tail = tail
        self.weight = weight
        self.group_id = group_id
        self.how = how
        self.remove = remove
        self.random = random
        self.iter_n = iter_n if self.random else 1
        self.reverse = reverse

        if metrics is None:
            metrics = nx.average_shortest_path_length
        self.metrics = tolist(metrics)

        # initialize graph
        self._init_graph() # self.G is dict

    def _init_graph(self):
        self.G = dict()
        for gro, data in self.data.items():
            g = nx.DiGraph()
            for i in range(len(data)):
                row = data.iloc[i]
                g.add_edge(row[self.head], row[self.tail], weight=row[self.weight])
            self.G[gro] = g

    @property
    def groups(self):
        return list(self.data.keys())

    @property
    def num_nodes(self):
        num_dict = {}
        for g in self.groups:
            num_dict[g] = self.G[g].number_of_nodes()

        return num_dict
            
    @property
    def num_edges(self):
        num_dict = {}
        for g in self.groups:
            num_dict[g] = self.G[g].number_of_edges()

        return num_dict

    def step(self, graph: nx.Graph, drop_num: int):
        """
        Attack for single graph.
        """
        g = deepcopy(graph)
        if self.random and self.how=="node":
            remove_random_nodes(graph=g, num=drop_num)
        elif self.random and self.how=="edge":
            remove_random_egdes(graph=g, num=drop_num)
        elif (not self.random) and self.how=="node":
            drop_nodes = [n for n, _ in sorted(list(g.degree()),
                                            key=lambda x: x[-1], reverse=self.reverse)[:drop_num]]
            remove_targeted_nodes(graph=g, nodes=drop_nodes)
        elif (not self.random) and self.how=="edge":
            drop_edges = [(h, t) for h, t, _ in sorted(list(g.edges(data="weight")),
                                                 key=lambda x: x[-1], 
                                                 reverse=self.reverse)[:drop_num]]
            remove_targeted_edges(graph=g, edges=drop_edges)
        else:
            raise ValueError("out of range")
        
        return g

    def evaluate(self, graph: nx.Graph):
        metrics = []
        for m in self.metrics:
            val = m(graph)
            metrics.append(val)
        return metrics

    def attack(
        self,
        num: Optional[int] = None,
        ratio: Optional[float] = None,
        verbose: bool = True,
        prog_bar: bool = True,
        **kwargs
    ):
        """
        Args:
            num (Optional[int]): number of nodes/edges are attacked
            ratio (Optional[float]): ratio of nodes/edges are attacked
        """
        if num is None and ratio is None: 
            raise ValueError("`num` and `ratio` could not be both None")
        if num is not None and ratio is not None:
            raise ValueError("`num` and `ratio` could not be both specified")

        assert num <= min(self.num_nodes.values()) if self.how == "node" else min(self.num_edges.values()),\
            "`num` is larger than minimum number"

        if verbose:
            print('{:-^26s}'.format("Attack starts!"))

        output_metrics = {}
        
        for group, graph in tqdm(self.G.items(), disable=not prog_bar):
            if ratio is not None:
                if self.how == "node":
                    num = math.floor(self.num_nodes[group] * ratio)
                else:
                    num = math.floor(self.num_edges[group] * ratio)

            raw_metric_list = []
            attacked_metric_list = []
            raw_metric = self.evaluate(graph) # evalute the raw graph
            raw_metric_list.append(raw_metric)
            for _ in range(self.iter_n):
                attacked_net = self.step(graph, drop_num=num) # attack the graph
                attacked_metric = self.evaluate(attacked_net) # evalute the attacked graph
                attacked_metric_list.append(attacked_metric)
            
            output_metrics.update({group: 
                {"raw": raw_metric_list,
                "attacked": attacked_metric_list,
                "squeezed": list_mean(attacked_metric_list)
                }
            })

        print('{:-^26s}'.format("Attack ends!"))

        self.output_metrics = output_metrics

        return output_metrics


    def plot(self, path: str = None, group: str = None):
        """
        Args:
            path (str): path to save image files
        """
        pass

    
    def summary(self, path: str = None):
        """
        Args:
            path (str): path to save summary files
        """
        pass