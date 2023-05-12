Playlist completion/song reccomendation on the spotify million playlist dataset https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/challenge_rules.  

Our approach creates a graph of all songs, albums and artists and uses a pagerank with teleports as the recommendation engine.
When using all the provided files, the number of nodes `n=3260226` and the number of edges `m=67662843`.  
With an intel core i7-7700 CPU @ 3.60 GHz and 16GB RAM, parsing the json file and constructing a networkX simple graph took around 37 minutes, then running `nx.pagerank(...)` on it for one example took around 77 minutes (however during the whole time, the computer was also in casual use).  
The output of the test run of the pagerank algorithm at first glance seems to be not quite perfect, but not bad either.  

TODO: check if there exist better methods/libraries/programs for dealing with such large graphs and performing pagerank on them or some other algorithm that could fulfill the recommendation/playlist completion task.