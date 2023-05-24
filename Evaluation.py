import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import timeit
import json
import random
import pickle
import os
import datetime

def evaluation_run(G,test_data_,generator_functions, different_starts = 1,persvec_lengths = [3,5],verbose=False,**kwargs):
    timer_start = timeit.default_timer()
    test_data = test_data_.copy()
    exceptions = 0
    global_counter = 0
    statistics = dict()
    
    if kwargs.get('ignore_short_playlists') == True:
        test_data = [i for i in test_data if len(i) > 9] ## in the challenge set file, the minimum number of playlist length ("num_tracks") is 10  
    

    #assert min([len(i) for i in test_data]) > persvec_lengths, "This will be a problem. Some playlists are shorter than the personalization vector. Pass ignore_short_playlists=True to run the simulation with reduced playlists."
    
    for function in generator_functions:
        for i in persvec_lengths:
            statistics[f"{str(function.__name__)} [{i} initials]"] = list()
    
    for test_playlist in test_data:
        for persvec_length in persvec_lengths:
            for _ in range(different_starts):
                persvec = [track['track_uri'] for track in random.sample(test_playlist,persvec_length)]
                try:
                    for function in generator_functions:
                        reccs = function.rank(None, G, personalization=persvec,**kwargs)

                        predicted_playlist = [reccs[i][0] for i in range(len(test_playlist)+persvec_length) if reccs[i][0] not in persvec]

                        ranking = len(set(predicted_playlist).intersection(set(p['track_uri'] for p in test_playlist)))/(len(predicted_playlist))
                        statistics[f"{str(function.__name__)} [{persvec_length} initials]"].append(ranking)
                    
                    if verbose:
                        time_elapsed = timeit.default_timer() - timer_start
                        mins_elapsed = (time_elapsed)//60
                        secs_elapsed = time_elapsed % 60
                        print(f"{100*(global_counter+exceptions+1)/(len(test_data)*len(persvec_lengths)*different_starts):02.1f}%; time elapsed: {mins_elapsed:02.1f} min {secs_elapsed:02.1f} sec", end="\r")
                    
                    global_counter+=1
                except Exception as e:
                    exceptions+=1
     
    if verbose:
        print()
        print(f"Number of exceptions (should be 0 in complete graph): {exceptions} out of {global_counter+exceptions} ({100*exceptions/(global_counter+exceptions):02.1f}%)")
    
    return statistics