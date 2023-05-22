import networkx as nx
import timeit
import json
import random
import pickle

def randWalkReccs(G, num_iterations=1000, walk_steps=10, personalization=None):
    ### personalization is an array with nodes to teleport to
    ### num iterations should be around 100*len(personalization)
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
            
    return reccs