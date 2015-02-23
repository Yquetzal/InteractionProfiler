from igraph import *
#import random as randr

from pylab import *
from time import *
import numpy as nump
from matplotlib import pyplot




def getReciprocalMessages(g):
	gMutual = Graph
	gMutual = g.copy()
	gMutual.to_undirected(mode="mutual",combine_edges="min")
	weights = gMutual.es["weight"]
	#sumWeights = sum(weights)*2
	weights = [i*2 for i in weights]
	return weights

def rewireKeepingLocalFriendShip(g):
	strengthBefore = g.strength(g.vs,mode="IN",weights="weight")
	#strengthBefore.sort(reverse=True)
	#print strengthBefore
	ess = g.es
	
	nbVertices = len(g.vs)
	gRewired = Graph(n=nbVertices,directed=True)
	
	inNodes = nump.random.randint(0,nbVertices,len(ess))
	
	outNodes = []
	i = 0
	for e in ess:
		outNodes.append( e.source)
		i=i+1
		
	
	listEdgesToAdd = []
	for i in range(len(outNodes)):
		inN = inNodes[i]
		outN = outNodes[i]
		if inN==outN:
			inN = nump.random.randint(0,nbVertices)
		listEdgesToAdd.append((int(inN),outN))
	
	#print(listEdgesToAdd)
	gRewired.add_edges(listEdgesToAdd)
	gRewired.es["weight"]= g.es["weight"]
	
	
	strengthRandom = gRewired.strength(gRewired.vs,mode="IN",weights="weight")
	#strengthAfter.sort(reverse=True)
	distBefore = getDistribution(strengthBefore)
	distRandom = getDistribution(strengthRandom)
	
	#sumDiff = 0
	#for i in range(len(strengthAfter)):
		#if(strengthBefore[i]>strengthAfter[i]):
			#sumDiff+=strengthBefore[i]-strengthAfter[i]
	#concentrationEffect = float(sumDiff)/sum(strengthBefore)
	(detail,concentrationEffect) = countStrength(distRandom,distBefore)
	concentrationEffect = concentrationEffect / float(sum(strengthBefore))
	####print "CONCENTRATION IMPACT:"+str(concentrationEffect)
	return concentrationEffect
	#print strengthAfter	
	#pouet = g.es["weight"]
	#pouet.sort(reverse=True)
	#print pouet
	#weights = ess["weight"]
	#outNodes = g.es.source
	

def getDistribution(weigths):
	if len(weigths)==0:
		repeated = [0]
		return repeated
	repeated = [0]*(int(max(weigths))+1)
	for w in weigths:
		repeated[int(w)]+=1
	return repeated

def countNbFriends(weightListRandom,weightListFriend):
	weightListRandom = weightListRandom + ([0]*(len(weightListFriend)-len(weightListRandom)))
	nbFriends = 0
	for i in range(len(weightListFriend)-1,0,-1):
		if(weightListFriend[i]>=weightListRandom[i]):
			nbFriends+=weightListFriend[i]-weightListRandom[i]
		else:
			break
	return nbFriends

def countStrength(distributionRandom,distributionFriend):
	#weightListRandom = weightListRandom + ([0]*(len(weightListFriend)-len(weightListRandom)))
	
	#nbFriends = 0
	#detailDiff = []
	#for i in range(len(weightListFriend)-1,0,-1):
		#if(weightListFriend[i]>=weightListRandom[i]):
			#nbFriends+=(weightListFriend[i]-weightListRandom[i])*i
			#detailDiff = detailDiff + [i]*(weightListFriend[i]-weightListRandom[i])
		#else:
			#break
	#return (detailDiff,nbFriends)
	strength = 0
	detailDiff = []
	for i in range(max(max(distributionRandom),max(distributionFriend))):
		if len(distributionFriend)>i:
			valueFriend = distributionFriend[i]
		else:
			valueFriend = 0
			
		if len(distributionRandom)>i:
			valueRand = distributionRandom[i]
		else:
			valueRand = 0			
		
		strength = max(0,strength + (valueFriend-valueRand)*i)
		detailDiff = (valueFriend-valueRand)*i
	return (detailDiff,strength)
	

def generateRandomNetwork(nbNodes,avgDeg):
	#generate the friendshipNetwork
	#friendPerNode = 10
	degrees = []
	for v in range(0,nbNodes):
		degree = avgDeg
		degrees.append(degree)
		
	g = Graph.Degree_Sequence(degrees,method="no_multiple")
	return g
	#summary(g)

def generateRandomForestFire(nbNodes):
	#generate the friendshipNetwork
	#friendPerNode = 10
	degrees = []
		
	g = Graph.Forest_Fire(nbNodes,0.42,0.45,3)
	return g
	#summary(g)


def loadNetwork(file):
	g = Graph.Read_Ncol(file,directed=True)
	
	g.es["weight"]= [1] *len(g.es)
	g.simplify(combine_edges=sum)	

	return g

def loadNetworkHead(file,n):
	with open(file) as f:
		lines = f.read().splitlines()
		listOfLists = []
		for l in lines:
			listOfLists.append(l.split("\t"))

		linksToLoad = listOfLists[:n]
		nodes = set()
		for link in linksToLoad:
		    nodes.add(link[0])
		    nodes.add(link[1])
		nodes=list(nodes)

		observedNetwork = Graph()
		observedNetwork.add_vertices(nodes)
		observedNetwork.add_edges(linksToLoad)
		
		observedNetwork.es["weight"]= [1] *len(observedNetwork.es)
		observedNetwork.simplify(combine_edges=sum)			
		return observedNetwork
	
def loadNetworkInMemory(file):
	start_time = time()
	
	with open(file) as f:
		lines = f.read().splitlines()
		listOfLists = []
		for l in lines:
			listOfLists.append(l.split("\t"))

		linksToLoad = listOfLists
		
	elapsed_time = time() - start_time
	#print("load full graph:"+str(elapsed_time))
	
	return linksToLoad


def loadNetworkHeadFromMemroy(links,n):
	start_time = time()
	
	linksToLoad = links[:n]
	nodes = set()
	for link in linksToLoad:
	    nodes.add(link[0])
	    nodes.add(link[1])
	nodes=list(nodes)

	observedNetwork = Graph(directed=True)
	observedNetwork.add_vertices(nodes)
	observedNetwork.add_edges(linksToLoad)
	
	observedNetwork.es["weight"]= [1] *len(observedNetwork.es)
	raw = observedNetwork.copy()
	observedNetwork.simplify(combine_edges=sum)		
	
	elapsed_time = time() - start_time
	#####print("from memory to graph object:"+str(elapsed_time))	
	return (raw,observedNetwork)

def generateCommunications(friendsNetwork,nbCommunications,friendStrength):
	#generate communication on friendshipNetwork
	nbVertices = friendsNetwork.vcount()
	gCom = Graph(n=nbVertices,directed=True)
	
	nbNotFriendsCommunications = float(1-friendStrength) * nbCommunications
	outNodes = nump.random.randint(0,nbVertices,nbNotFriendsCommunications)
	inNodes = nump.random.randint(0,nbVertices,nbNotFriendsCommunications)
	
	nbFriendCommunication = nbCommunications - nbNotFriendsCommunications
	adjList = friendsNetwork.get_adjlist(mode="out")
	listOutNodeFriend = nump.random.randint(0,nbVertices,nbFriendCommunication)
	listInNodeFriend = []
	for com in listOutNodeFriend:
		choice = adjList[com]
		if len(choice)>0:
			selectedInNode = choice[random.randint(0,len(choice))]
		else:			
			selectedInNode = random.randint(0,nbVertices)
		listInNodeFriend.append(selectedInNode)
	outNodes = concatenate([outNodes,listOutNodeFriend])
	inNodes = concatenate([inNodes,listInNodeFriend])
	
	listEdgesToAdd = []
	for i in range(len(outNodes)):
		inN = inNodes[i]
		outN = outNodes[i]
		if inN==outN:
			outN = nump.random.randint(0,nbVertices)
		listEdgesToAdd.append((int(inN),outN))
	
	#print(listEdgesToAdd)
	gCom.add_edges(listEdgesToAdd)
	gCom.es["weight"]= [1] *len(gCom.es)
	
	gComRaw = gCom.copy()	
	gCom.simplify(combine_edges=sum)
	return (gComRaw,gCom)

def rewireCommunicqtion(rawGraphToRrewire):
	#rawGraphToRrewire.rewire_edges(1)
	rewired = Graph.Degree_Sequence(rawGraphToRrewire.degree(mode="out"),rawGraphToRrewire.degree(mode="in"))
	rewired.es["weight"]= [1] *len(rewired.es)
	
	rewired.simplify(combine_edges=sum)
	return rewired

#def getListOfRandomEdges(aGraph,nbEdgesWanted):
	#nbVertices = friendsNetwork.vcount()
	
	#outNodes = random.randint(0,nbVertices,nbEdgesWanted)
	#inNodes = random.randint(0,nbVertices,nbEdgesWanted)	
	#listEdgesToAdd = []
	#for i in range(len(outNodes)):
		#inN = inNodes[i]
		#outN = outNodes[i]
		#if inN==outN:
			#outN = random.randint(0,nbVertices)
		#listEdgesToAdd.append((int(inN),outN))	
	
def rewireWithFriendShip(rawGraphToRrewire,friendShipGRaph,friendStrength):
	
	#rewire whole graph
	rewired = Graph.Degree_Sequence(rawGraphToRrewire.degree(mode="out"),rawGraphToRrewire.degree(mode="in"))
	#delete the appropriate number of edges
	nbEdgesToChange = round(friendStrength*float(len(rawGraphToRrewire.es)))
	edgesToDelete = nump.random.choice(range(len(rewired.es)), nbEdgesToChange,replace=False) 
	rewired.delete_edges(edgesToDelete)
	
	#add the appropriate number of edges from friendShip network	
	allFriendShips = friendShipGRaph.get_edgelist()
	chosenFriendShips = nump.random.randint(0,len(allFriendShips),nbEdgesToChange)
	listEdgesToAdd = []
	
	for i in range(len(chosenFriendShips)):
		inN = allFriendShips[chosenFriendShips[i]][0]
		outN = allFriendShips[chosenFriendShips[i]][1]
		listEdgesToAdd.append((inN,outN))	
	rewired.add_edges(listEdgesToAdd)
	
	rewired.es["weight"]= [1] *len(rewired.es)
	
	raw = rewired.copy()
	rewired.simplify(combine_edges=sum)
	return (raw,rewired)

#def generateCommunicationsOLD(friendsNetwork,nbCommunications,friendStrength):
	##generate communication on friendshipNetwork
	#nbVertices = friendsNetwork.vcount()
	#gCom = Graph(nbVertices)
	
	#listEdgesToAdd = []
	#for com in range(0,nbCommunications):
		##print com
		#selectedOutNode = randrange(nbVertices)
		#selectedInNode = -1
		#if uniform(0,1)>friendStrength:
			#choice = range(0,nbVertices)
			#choice.remove(selectedOutNode)
			#selectedInNode = choice[randrange(nbVertices-1)]
		#else:
			#choice = friendsNetwork.neighbors(selectedOutNode)
			#selectedInNode = choice[randrange(len(choice)-1)]
		#listEdgesToAdd.append((selectedOutNode,selectedInNode))
		
	#gCom.add_edges(listEdgesToAdd)
	#gCom.es["weight"]= [1] *len(gCom.es)
	#gCom.simplify(combine_edges=sum)
	#return gCom

#def generateCommunicationsRandomFast(friendsNetwork,nbCommunications):
	#start_time = time()
	##generate communication on friendshipNetwork
	#nbVertices = friendsNetwork.vcount()
	#gCom = Graph(nbVertices)
	

	
	#listEdgesToAdd = []
	#for com in range(0,nbCommunications):

		#selectedOutNode = randrange(nbVertices)
		#selectedInNode = randrange(nbVertices)
		
		#while(selectedInNode==selectedOutNode):
			#selectedOutNode = randrange(nbVertices)
			#selectedInNode = randrange(nbVertices)	
		
		#listEdgesToAdd.append((selectedOutNode,selectedInNode))
		
	#elapsed_time = time() - start_time
	#print("generate list of edges:"+str(elapsed_time))
	#start_time = time()
	
	#gCom.add_edges(listEdgesToAdd)
	#gCom.es["weight"]= [1] *len(gCom.es)
	
	#elapsed_time = time() - start_time
	#print("creating network:"+str(elapsed_time))	
	#start_time = time()
	
	#gCom.simplify(combine_edges=sum)
	#elapsed_time = time() - start_time
	#print("simplify operation:"+str(elapsed_time))	
	
	#return gCom


saveForGraphX = []
saveForGraphY = []
saveForGraphX2 = []
saveForGraphY2 = []

def compareTwoNetworks(NetRandom,NetObserved,plotFigure=False):
	nbCommunications = sum(NetObserved.es["weight"])
	#print("nbComInNetComputed:"+str(nbCommunications))
	nbNodes = len(NetObserved.vs)
	maxPossibleEdges = (nbNodes*(nbNodes-1))/2
	
	weights1 = NetObserved.es["weight"]
	observed = getDistribution(weights1)
	
	weights2 = NetRandom.es["weight"]
	maxWeight = max(weights2)
	
	#print(" certain friendship")
	#countSupThreashold = filter(lambda x: x>1+maxWeight,weights1)
	#print(len(countSupThreashold))
	#print(sum(countSupThreashold)/float(nbCommunications))
	
	random = getDistribution(weights2)	
	
	nbFriendsEstimate = countNbFriends(random,observed)
	
	
	
	
	#print("++++")
	(detailDiff,strengthRaw) = countStrength(random,observed)
	
	#print(strengthRaw)
	strengthRaw = strengthRaw #- nbFriendsEstimate*(nbCommunications/(maxPossibleEdges*2))
	#print(strengthRaw)
	
	strengthFriendsEstimate = strengthRaw/float(nbCommunications)
	#print(strengthFriendsEstimate)
	
	#modification: return the number fo friends per user
	nbFriendsEstimate = nbFriendsEstimate/float(nbNodes)	
	xLength = len(observed)
	random = random+[0]*xLength
	
	if plotFigure:
		fig = pyplot.figure()
		#toPlot = nump.subtract(observed[2:xLength],random[2:xLength])
		toPlot = observed
		
		for x in range(len(toPlot)):
			if toPlot[x]<0:
				toPlot[x]=0
				
		percentCom = range(len(toPlot))
		
		#percentCom = range(2,xLength)
		#percentCom = nump.cumsum(percentCom)
		#percentCom = nump.divide(percentCom,float(nbCommunications))
		#percentCom = nump.divide(percentCom,float(nbCommunications/nbNodes)) # problem, because not homogeneous nodes
		toPlotCopy = toPlot[::-1]
		plot(range(0,len(observed)),observed,label="observed")
		plot(range(0,len(random)),random,label="null model")
		yscale("log")
		xscale("log")		
		ylabel("Frequency")
		xlabel("Repeated communications")
		legend(loc="upper right")
		
		show()
		
		#CHART OF DISTRIBUTION OF CONCENTRATION (OTHER)		
		toPlotPercent = nump.multiply(percentCom,toPlot)
		toPlotPercent = toPlotPercent[::-1]
		toPlot = toPlot[::-1]
		
		
		toPlotPercent = nump.cumsum(toPlotPercent)
		
		toPlotPercent = nump.divide(toPlotPercent,float(nbCommunications)) # problem, because not homogeneous nodes
		
		
		toPlot = nump.cumsum(toPlot)
		#toPlot = nump.cumsum(toPlot[::-1])[::-1]
		
		toPlot = nump.divide(toPlot,float(nbNodes))
		
		
		saveForGraphX.append(toPlotPercent)
		saveForGraphY.append(toPlot)
		###for i in range(len(saveForGraphX)):
			###plot(saveForGraphX[i],saveForGraphY[i],label=str(i))
		
		#legend(loc="top left")
		#yscale("log")
		#xscale("log")
		show()
	
		print(observed[:100])
		
		
		
		#fig = pyplot.figure()
	
		#plot(range(0,xLength),observed[:xLength],label="withFriends")
		#plot(range(0,xLength),random[:xLength],label="random")
		
		#legend(loc="upper right")

		#show()
	
		#print(observed[:100])


	nos = NetObserved.es["weight"]
	nra = NetRandom.es["weight"]
	nos.sort(reverse=True)
	nra.sort(reverse=True)

	
	sumDiff=0
	for i in range(len(nos)):
		if(nos[i]>nra[i]):
			sumDiff+=nos[i]#-nra[i]
	concentrationEffect = float(sumDiff)/sum(nos)
	#print "THIS IS Q TEST "+str(strengthFriendsEstimate)

	return (nbFriendsEstimate,strengthFriendsEstimate)
	
	
	


#random
#nbComs = 1000
#pFriend = 0
#gRand = Graph(n)

#listEdgesToAdd = []
#for com in range(0,nbComs):
	#selectedOutNode = randrange(n)
	#selectedInNode = -1
	#if uniform(0,1)>pFriend:
		#choice = range(0,n)
		#choice.remove(selectedOutNode)
		#selectedInNode = choice[randrange(n-1)]
	#else:
		#choice = g.neighbors(selectedOutNode)
		#selectedInNode = choice[randrange(len(choice)-1)]
	#listEdgesToAdd.append((selectedOutNode,selectedInNode))
	
#gRand.add_edges(listEdgesToAdd)
#gRand.es["weight"]= [1] *len(gRand.es)
#gRand.simplify(combine_edges=sum)

#def findForestFireOFGivenAverageDegree(nbNodes,objectiveDegree):
#	initialParameters =(0.3,

def computeFriendShipPureRandom(nbNodes,nbFriends,friendShip,nbObservedCommunication ):
	avgOutDegree = nbFriends
	friendStrength = friendShip
	nbActors = nbNodes
	maxPossibleEdges= (nbActors*(nbActors-1))/2
	
	
	#friendshipNetwork = generateRandomNetwork(nbActors,avgDegree)
	#friendshipNetwork = generateRandomForestFire(nbActors)
	friendshipNetwork = Graph.Static_Power_Law(nbActors,int(round(nbActors*avgOutDegree)),2.5,2.5)
	#print("summary friendShip network")
	#summary(friendshipNetwork)

	
	
	estNbFriendShips = []
	estFriendShipStrength = []
	
	croisssancesStep = nbObservedCommunication

	
	for coms in croisssancesStep:
		nbCommunications = coms
		#print("nbComContruction: "+str(nbCommunications))
	
		(gRaw,gComFriends) = generateCommunications(friendshipNetwork,nbCommunications,friendStrength)
		#print("communications with friendship")
		
		
		
		#summary(gComFriends)
		weights = gComFriends.es["weight"]
		degsFriends = getDistribution(weights)
	
	
		#gComRand = generateCommunicationsRandomFast(gComFriends,nbCommunications)	
		#gComRand = generateCommunications(friendshipNetwork,nbCommunications,0)
		gComRand = rewireCommunicqtion(gRaw)
		
		#print("communications without friendship")
		
		
		
		#summary(gComRand)
		weights = gComRand.es["weight"]
		degsRandom = getDistribution(weights)
		
		
		
		
		
		(nb,ratio) = compareTwoNetworks(gComRand,gComFriends)
		estNbFriendShips.append(nb)
		estFriendShipStrength.append(ratio)
		
		nbFriendsEstimate = countNbFriends(degsRandom,degsFriends)
		#print("--------")
		
		strengthRaw = countStrength(degsRandom,degsFriends)
		strengthRaw = strengthRaw - nbFriendsEstimate*(nbCommunications/(maxPossibleEdges*2))
		strengthFriendsEstimate = strengthRaw/float(nbCommunications)
		
		#print("nbfriendsEstimate:"+str(nbFriendsEstimate))
		#print("strengthFriendShipEstimate:"+str(strengthFriendsEstimate))
		#estNbFriendShips.append(nbFriendsEstimate)
		#estFriendShipStrength.append(strengthFriendsEstimate)
		
	return(estNbFriendShips,estFriendShipStrength)

def gini(list_of_values):
	sorted_list = sorted(list_of_values)
	height, area = 0, 0
	for value in sorted_list:
		height += value
		area += height - value / 2.
	fair_area = height * len(list_of_values) / 2
	return (fair_area - area) / fair_area

def evaluateReciprocity(g):
	reciprocal = 0;
	edges = g.es
	edgesW = g.es["weight"]
	for i in range(len(edges)):
		if edgesW[i]>=2:
			edge = edges[i]
			endpoints = edge.tuple
			oppositeEdge = g.get_eid(endpoints[1],endpoints[0],error=False)
			if oppositeEdge>=0:
				if edgesW>=2:
					reciprocal+=1
	
	reciprocal = reciprocal/2
	
	return reciprocal
				
			
			
		
	
	