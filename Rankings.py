from abc import ABC, abstractmethod
from typing import List, Tuple
from colorama import Fore
import networkx as nx
import numpy as np
import random
import re
import timeit

class RankingFunctionInterface(ABC):
    @abstractmethod
    def rank(self, G, personalization=None, **kwargs) -> List[Tuple[str, int]]:
        pass
    
class RandomWalk(RankingFunctionInterface):
    def rank(self, G, personalization=None, **kwargs):
        num_iterations = 1000
        if personalization is not None:
            num_iterations = 100*max(len(personalization),10)
        elif kwargs.get('num_iterations') is not None and type(kwargs.get('num_iterations')) is int:
            num_iterations = kwargs.get('num_iterations')

        walk_steps = 10
        if kwargs.get('walk_steps') is not None and type(kwargs.get('walk_steps')) is int:
            walk_steps = kwargs.get('walk_steps')

        reccs = {}
        for i in range(num_iterations):
            if personalization != None:
                start_node = random.choice(personalization)
            else:
                start_node = random.choice(list(G.nodes()))

            if (start_node not in reccs.keys()):
                reccs[start_node] = 1
            else:
                reccs[start_node] = reccs[start_node] + 1

            for j in range(walk_steps):
                tmp_node = random.choice(list(G.neighbors(start_node)))
                if (tmp_node not in reccs.keys()):
                    reccs[tmp_node] = 1
                else:
                    reccs[tmp_node] = reccs[tmp_node] + 1
                start_node = tmp_node


        rec_songs = filter(lambda x: str.startswith(str(x[0]), "track:"), reccs.items())
        reccs_sorted = sorted(rec_songs, key=lambda x: x[1], reverse=True)
        return reccs_sorted
    
class PreferentialAttachment(RankingFunctionInterface):
    def rank(self, G, personalization=None, **kwargs):
        if personalization is None:
            print(Fore.RED + 'Warning: Running preferential Attachment without a personalization vector makes no sense!')
            return []
        
        G.add_node("test_playlist")
        for track in personalization:
            G.add_edge("test_playlist", track)

        edges_to_predict = [('test_playlist',node) for node in list(G.nodes()) if bool(re.search(r'track',str(node)))]
        predictions = list(nx.preferential_attachment(G, edges_to_predict))
        chosen = sorted([p for p in list(predictions) if p[2] > 0], key = lambda x: x[2], reverse=True) 
        G.remove_node("test_playlist")

        return [(p[1],p[2]) for p in chosen]