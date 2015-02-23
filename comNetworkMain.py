import os
import sys

sys.path.append(os.path.abspath("tools"))
from functionsComNet import *
import cProfile
import argparse


###############################################
#            EVALUATE REAL NETWORK
###############################################
parser = argparse.ArgumentParser(description="launchEvaluation")
parser.add_argument("networkFile",action="store")
parser.add_argument("-l", "--limit", help="Specifiy a limit to the number of interactions to consider. All by default",action="store")
parser.add_argument("-s","--steps",help="Choose the number of steps to compute (default: 10)",action="store")
args = parser.parse_args()



	
file=args.networkFile

edgesInMemory = loadNetworkInMemory(file)	

#default limit is all file, but can be modified.
limit = len(edgesInMemory)
if args.limit:
	limit=int(args.limit)
	
#default nb step is 10, can be modified
inc = 	inc=int(limit)/10
if args.steps:
	inc=int(limit)/int(args.steps)

def evalRealNet():
	croisssancesStep = []
		
	#inc = 10000000 #3000000
	#limit = 10000000
	#file = "tzitterPureRTPrecise.ncol"	
	
	
	print ("loading file")
	
	
	i=inc
	while(i<=limit):
		croisssancesStep.append(i)
		i=i+inc
		
	listRatio = []
	listrecip = []
	listConcentration = []
	
	
	
	
	
	comByUser = []
	for i in croisssancesStep:
		
		#load head of a network
		print ("    ------")
		
		print ("(create network object (nbInteractions= "+str(i)+"))")
		#print(i)
		(rawObserved,observedNetwork) = loadNetworkHeadFromMemroy(edgesInMemory,i)
		nbCommunications = sum(observedNetwork.es["weight"])
		#print(sum(observedNetwork.es["weight"]))
		#print(len(rawObserved.es))
		
		reciprocalObserved = getReciprocalMessages(observedNetwork)
		#print("percentOfReciprocal "+str(reciprocal))
		
		#this function also compute and display the CONCENTRATION impact
		concentrationEffect = rewireKeepingLocalFriendShip(observedNetwork)
		
		
		nbActors = len(rawObserved.vs)		
		###################OPTIONAL PART TO TEST METHOD#########
		#friendshipNetwork = Graph.Static_Power_Law(nbActors,int(round(nbActors*5)),2.5,2.5,multiple=False)
		#(rawObserved,observedNetwork) = rewireWithFriendShip(rawObserved,friendshipNetwork,0.39)
		########################################################
		comByUser.append(float(i)/nbActors)
	
		#print ("network created")
		
		#print observedNetwork.degree_distribution()
		#print(len(rawObserved.es))
		
		#print nbCommunications
		#print summary(observedNetwork)
		print "interaction per node = "+str(nbCommunications/float(nbActors))
		
		
		#randomised = generateCommunications(observedNetwork,nbCommunications,0)
		print ("(randomizing network)")
		
		#randomised = generateCommunicationsRandomFast(observedNetwork,nbCommunications)
		#randomised = generateCommunications(observedNetwork,nbCommunications,0)
		randomised  = rewireCommunicqtion(rawObserved)
		
		
		#print "randomisation done"
		#print summary(randomised)
		reciprocalRANDOM = getReciprocalMessages(randomised)
		
		#print("percentOfReciprocalRANDOM "+str(reciprocalRANDOM))
		#print("RECIPROCAL "+str(reciprocal-reciprocalRANDOM))
		(detail,reciprocal) = countStrength(getDistribution(reciprocalRANDOM),getDistribution(reciprocalObserved))
		
		
		(nb,ratio) = compareTwoNetworks(randomised,observedNetwork,False)
		#listNb.append(nb)
		listRatio.append(ratio)
		print("SOCIAL STRUCTURE IMPACT(SSI): "+str(ratio))
		
		reciprocity = reciprocal/float(nbCommunications)
		print ("RECIPROCITY IMPACT(RI)"+str(reciprocity))
		listrecip.append(reciprocity)
		
		print "CONCENTRATION IMPACT(CI):"+str(concentrationEffect)
		listConcentration.append(concentrationEffect)
		
		
		#reciprocity = evaluateReciprocity(observedNetwork)
		#print(nb*nbActors)
		#print(reciprocity)
		#print(reciprocity*2/float(nb*nbActors))
	
	subplot(3,1,1)
	#plot(croisssancesStep[:len(listNb)],listNb)
	plot(comByUser,listRatio)
	ylim([0,1])
	ylabel("SSI")
	
	
	subplot(3,1,2)
	plot(comByUser,listrecip)
	ylim([0,1])
	ylabel("RI")
	
	
	subplot(3,1,3)
	plot(comByUser,listConcentration)	
	#plot(croisssancesStep[:len(listNb)],listRatio)
	ylim([0,1])
	ylabel("CI")
	
	#draw()	
	show()		
	
evalRealNet()

#cProfile.run("evalRealNet()")
