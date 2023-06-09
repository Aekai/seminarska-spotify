import networkx as nx
import pandas as pd
import numpy as np
import timeit
import json
import random
import datetime
import pickle
import os

def sample_graph(num_files=15,**kwargs):
    """ Return a random subsample of the spotify playlist
    graph.
    
    Parameters
    ------------
        num_files: int, Optional
            The number of original files out of 1.000 from which
            a sample will be built. Default is set to 15
        verbose: bool, Optional
            Wheater you want the progress to be documented and the
            total time to be printed at the end. Default is False
        include_artists: bool, Optional
            Whether artist nodes should be included in the sampled graph.
            Default is True
        include_albums: bool, Optional
            Whether album nodes should be included in the sampled graph.
            Default is True
        
    Return
    -----------
        Graph : networkx.Graph or networkx.DiGraph
            The sampled graph.
    """
    if kwargs.get('verbose') == True:
        timer_start = timeit.default_timer()
       
    trim_start = len("spotify:")
    path = "./DATA/"
    if kwargs.get('path') is not None:
        path = kwargs.get('path')
    files = random.sample([x for x in os.listdir(path)],num_files)
    
    # timestamp_threshold = pd.Timestamp("2017-09-15 00:00:00") # 75% data -- 249413 playlists in test set
    # timestamp_threshold = pd.Timestamp('2017-10-03T00:00:00.000000000') # 80% data -- 198144 playlists in test set
    # timestamp_threshold = pd.Timestamp("2017-10-01 00:00:00") # last month only -- 205220 playlists in test set
    timestamp_threshold = pd.Timestamp("2017-10-31 00:00:00") # last day only -- 4372 playlists in test set
    test_playlists = []
    
    #TODO: directed switch?
    G = nx.Graph()
    for i,file in enumerate(files):
        with open(f"{path}{file}") as read_file:
            tmp = json.load(read_file)
            for playlist in tmp["playlists"]:
                #TODO: ignore newer switch?
                if kwargs.get('testSplit') == True:
                    if (datetime.datetime.fromtimestamp(playlist["modified_at"]) > timestamp_threshold):
                        test_playlists.append(playlist)
                        continue

                G.add_node(playlist["pid"], playlist_name=playlist["name"], TYPE="PLAYLIST", modified_at=playlist["modified_at"])
                for track in playlist["tracks"]:
                    track_id = track["track_uri"][trim_start:]
                    G.add_node(track_id, track_name=track["track_name"], artist_name=track["artist_name"], TYPE="TRACK")
                    G.add_edge(track_id, playlist["pid"])
                    
                    artist_id = track["artist_uri"][trim_start:]
                    album_id = track["album_uri"][trim_start:]
                    
                    if kwargs.get('include_albums',True) == True:
                       
                        G.add_node(album_id, album_name=track["album_name"], TYPE="ALBUM")
                        G.add_edge(album_id, track_id)
                        if kwargs.get('include_artists',True) == True:
                            G.add_node(artist_id, artist_name=track["artist_name"], TYPE="ARTIST")
                            G.add_edge(artist_id, album_id)
                            
                    else:
                        if kwargs.get('include_artists',True) == True:
                            G.add_node(artist_id, artist_name=track["artist_name"], TYPE="ARTIST")
                            G.add_edge(artist_id, track_id)
                 
            if kwargs.get('verbose') == True:
                time_elapsed = timeit.default_timer() - timer_start
                mins_elapsed = (time_elapsed)//60
                secs_elapsed = time_elapsed % 60
                print(f"{i+1}/{len(files)}; time elapsed: {mins_elapsed:02.1f} min {secs_elapsed:02.1f} sec", end="\r")
                    
                    
                    
                
    if kwargs.get('verbose') == True:
        timer_stop = timeit.default_timer()
        print()
        print('Time elapsed:', (timer_stop - timer_start)//60, "min ", time_elapsed % 60, "sec")  
        print(f"n:{G.number_of_nodes()}, m:{G.number_of_edges()}; ")
    
    if kwargs.get('testSplit') == True:
        print(len(test_playlists), "test playlists; mean len:", np.mean([len(i) for i in test_playlists]))
        print("num test playlists with len > 9:", len([1 for i in test_playlists if len(i) > 9]))
        return (G, test_playlists)

    return G

def get_modified_at_array(G, print_hist=False):
    playlist_times = []
    for node in G.nodes():
        if type(node) == int:
            playlist_times.append(G.nodes[node]["modified_at"])
    
    ser = pd.Series(playlist_times)
    ser = pd.to_datetime(ser, unit='s')

    if (print_hist==True):
        ser.hist(xrot=90, bins=20)

    return ser

def truncate_playlists(playlists):
    new_playlists = list()
    for playlist in playlists:
        new_playlist = list({'name': f"{i['artist_name']} - {i['track_name']}", 'track_uri': i['track_uri'][len("spotify:"):]} for i in playlist['tracks'])
        new_playlists.append(new_playlist)
    
    return new_playlists