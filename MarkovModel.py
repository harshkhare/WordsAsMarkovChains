# This program builds nth order Markov model

import sys
import re
#from collections import defaultdict
import numpy as np
import random
import pickle
import warnings

#Not used
#def infinite_defaultdict():
#	return defaultdict(infinite_defaultdict)
### END infinite_deraultdict() ###

#####################################################################

class MarkovModel:
	def __init__(self, verbose=False):

    #Initialize golbal variables with None
		self.verbose = verbose
		self.filename = None
		self.from_file = False
		self.states = None
		self.order = None
		self.seqs = None
		self.nstates = None
		self.stateCount = None
		self.transitionCountMat = None
		self.transitionProbMat = None
		self.transitionProbMat_cumsum = None

		#Ignore warnings
		warnings.simplefilter("ignore")

		print("Class",self.__class__.__name__,":: Instance created.\n") if self.verbose else ""
 ###END __init__ ###

	def fit(self,state_sequences=None,states=None,order=None,filename=None,from_file=False):
		#Fit model to data. In this case, calculate transition probability matrices.
		self.filename = filename
		self.from_file = from_file

		if not from_file:
		#Fit model to data if model is not read from file
			self.states = states
			self.order = order
			self.seqs = []
			for seq in state_sequences:
				self.seqs.append(['^']*self.order+seq)
			self.nstates = len(self.states)

			#print(self.seqs,"\n",self.states)

			#Create array to hold state frequencies
			self.stateCount = np.zeros(self.nstates)

			#Create state transition matrices
			#print("Generating",self.order+1,"dimensional square matrices for",self.nstates,"states.")
			self.transitionCountMat = np.zeros(tuple([int(i) for i in np.zeros(self.order+1)+self.nstates]))
			self.transitionProbMat = np.zeros(tuple([int(i) for i in np.zeros(self.order+1)+self.nstates]))
			self.transitionProbMat_cumsum = np.zeros(tuple([int(i) for i in np.zeros(self.order+1)+self.nstates]))

			#Testing the matrices
			#print(self.transitionCountMat)
			#self.transitionCountMat[tuple([2,0,3])] = 123
			#print(self.transitionCountMat)

			#Count occurrenes of the state combinations depending upon the selected order of the Markov Model.
			#For 2nd order Markov Model, we have 3D array which holds counts of occurrences of triplets.
			#Example: For triplet 'ACD', 'AC' decide the probability of 'D' to occur next. Hence a 3D array is required to hold counts of all 'D's that occur following 'AC'.
			for seq in self.seqs:
				#print(seq, list(range(self.order,len(seq))))
				for i in range(self.order,len(seq)):

					#Calculate state counts
					self.stateCount[self.states.index(seq[i])] += 1

					#Calculate state transition counts
					#print("State sequence: ",seq[i-self.order:i] + seq[i],end="       ")
					#print("State indices:",[self.states.index(state) for state in seq[i-self.order:i]] + [self.states.index(seq[i])])
					self.transitionCountMat[ tuple([self.states.index(state) for state in seq[i-self.order:i]] + [self.states.index(seq[i])]) ] += 1

			#Calculate probabilities based on the counts
			#print(self.transitionCountMat.sum(axis=self.order).T)
			self.transitionProbMat = (self.transitionCountMat.T / self.transitionCountMat.sum(axis=self.order).T).T

			#Calculate cumulative sums of probabilities which will help in gneration of new state sequence based on the model.
			self.transitionProbMat_cumsum = np.cumsum(self.transitionProbMat,axis=self.order)

		else:
			#Load model from file
			self.load(fname=filename)

		#Set this option to print full numpy arrays
		np.set_printoptions(threshold=sys.maxsize)

		#Print matrices
		#print(self.transitionCountMat)
		#print("------------------------------------------------------------------")
		#print(self.transitionProbMat)
		#print("------------------------------------------------------------------")
		#print(self.transitionProbMat_cumsum)

		#Write model matrices to file
		with open("MarkovModel_matrices.model",'w') as f:
			f.write("#Transition Count Matrix:\n")
			f.write(str(self.transitionCountMat))
			f.write("\n\n")
			f.write("#Transition Probability Matrix:\n")
			f.write(str(self.transitionProbMat))
			f.write("\n\n")
			f.write("#Transition Probability Cumulative Sum Matrix:\n")
			f.write(str(self.transitionProbMat_cumsum))
			f.write("\n\n")
 ### END fit ###

	def predict(self,seq):
		#Predict next state based on the provided sequence of states

		#Check for minimum number of states needed to predict the next state
		if len(seq) < self.order:
			return(None)

		#print(seq,seq[-self.order:][0],seq[-self.order:][1])
		#print(tuple([self.states.index(state) for state in seq[-self.order:]]))
		#print(self.transitionProbMat_cumsum[ tuple([self.states.index(state) for state in seq[-self.order:]] + [0]) ])

		#Generate a random number and compare against cumulative transition probabilities for the previous m steps, where m is the order of Markov Model.
		#Return the predicted state.
		r = random.uniform(0,1)
		for i in range(0,self.nstates):
			#print(self.transitionProbMat_cumsum[ tuple([self.states.index(state) for state in seq[-self.order:]] + [i]) ])
			if r <= self.transitionProbMat_cumsum[ tuple([self.states.index(state) for state in seq[-self.order:]] + [i]) ]:
				#print(r, self.states[i])
				return(self.states[i])
		#print("Warning: '"+seq[-self.order:]+"' was either not present in the training data or had very low frequency.")
		return(None)
### END predict ###

	def generate(self,length=3,forced=False):
		#Generate a random state sequence based on the model
		#
		#forced=True will trigger regeneration of the sequence if the predict function returns None.
		#This will ensure the length of the returned sequence.

		#Start with sequence of '^' symbols
		seq = ['^']*self.order

		#Predict next state till the length criterion is matched and return the generated state sequence excluding the '^' symbols.
		i = 0
		while(i < length):
			#print(seq)
			state = self.predict(seq)
			if state != None:
				seq.append(state)
				i += 1
			elif forced:
				#Restart if next state cannot be predicted and forced==True
				seq = ['^']*self.order
				i =0
			else:
				i += 1
		#print(i,seq)

		return(seq[self.order:])
### END generate ###

	def tofile(self,filename=None):
		#Dump model to file
		print("Dumping model to file:",filename,"(This does not save training data.)") if self.verbose else ""
		with open(filename, 'wb') as output:
			pickle.dump([self.states, self.order, self.nstates, self.stateCount, self.transitionCountMat, self.transitionProbMat, self.transitionProbMat_cumsum],
									output,
									pickle.HIGHEST_PROTOCOL)
	### END tofile ###

	def load(self,fname=None):
		#Load model from file
		print("Loading model from file:",fname) if self.verbose else ""
		with open(fname, 'rb') as infile:
			[self.states, self.order, self.nstates, self.stateCount, self.transitionCountMat, self.transitionProbMat, self.transitionProbMat_cumsum] = pickle.load(infile)
	### END load ###

###### END Class MarkovModel ######





