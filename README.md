# InteractionProfiler
This code can be used to compute three caracteristics of the nature of interactions between a set of actors.
Details can be found in my publications, that you can find on my website http://cazabetremy.fr

Three values are computed:
* Social Structure Impact(SSI): how strong is the influence of the social structure on the interactions between authors, compared with random interactions
* Concentration Impact(CI): how much concentration there is in the interactions, excluding interpersonal friendships (strong if a few actors receive most of interactions)
* Reciprocity Impact(RI): how strong is the reciprocity in interactions between users.
All these values can take values between 0 and 1, 0 meaning that obesrvations can be explained by random interactions, 1 meaning that none of the observations can be expplained by random interactions.

The data you need to provide to the program is simply a list of pairs of interactions: 
* ActorX  ActorY
* ActorZ actorXX
* ActorX actorY
* ...

It also corresponds to the edgelist format or the ncol format in graphs. Repeated interactions are possible. (well, more that possible, needed...)

To run the program, the basic command is:

`python YOUR_FILE` 

this will run the program, giving you a partial results every time 1/10 of the file has been processed.
At the end, some plots show you how the values changed. The plots should tend to a stabilization, otherwise it means that you do not hav enough data... or that the method has a flaw. In this case, do not hesitate to send your comments !

There are two optional parameters to the program
* `-l INT`  (a limit to the number of interactions to consider. You can use it if your file takes too much time to process, to have a partial result)
* `-s INT` (the number of steps to make. Default 10. More steps means a slower computation but more partial results. Less steps means faster computation, less partial results.
