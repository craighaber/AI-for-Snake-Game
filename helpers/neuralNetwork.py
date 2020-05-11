#*********************************************************************************
#neuralNetwork.py
#Author: Craig Haber
#5/9/2020
#This module contains functions for a neural network with 2 hidden layers made
#entirely from scratch.
#The weights are generated through training the genetic algorithm 
#geneticAlgorithm.py in snakeGameGATrain.py.
#*********************************************************************************

import random
import itertools
import math

def mapChrom2Weights(chrom, bitsPerWeight, numInputs, numHiddenLayerNodes, numOutputs):
	"""Function to initialize the structure of the list of weights.
	
	Specifically, this function is called from mapChrom2Weights so that the 
	chromsosome bit string can be translated into a list structure.

	Arguments:
		chrom: A string of bits representing all of the weights for the neural network.
		bitsPerWeight: the number of bits that are dedicated to a single weight in chrom
		numOuputs: the number of outputs in the neural network
		numInputs: the number of inputs in the neural network
		numHiddenNodes: the number of nodes in each of the 2 hidden layers in the neural network
		numOuputs: the number of outputs in the neural network

	Returns:
		weightList:  A list where each element represents the weights for a layer in the network.
		It always contains 3 lists: the first for weights between the input layer and hidden layer 1,
		the second for the weights between hdden layer 1 and hidden layer 2,
		and the third for the weights between hidden layer 2 and the output layer.
		Also, each of these 3 lists consists of lists representing all the weights going into a specific node in 
		the network.

	"""

	weightList = initializeWeightList(numInputs, numHiddenLayerNodes, numOutputs)

	#Add an empty space at the beginning of the string for the sake of using 1-based indexing
	chrom  =  " " + chrom
	
	#Calculate/store weights from input to hidden layer 1
	#First, determine where the bits representing the weights for hidden layer 1 end (add 1 to numInputs to include threshold)
	hiddenLayer1BitsEnd = bitsPerWeight*(numInputs+1)*numHiddenLayerNodes
	index = 1
	node_num = 0
	numWeightsPerCurNode = 0

	#While we are still looking at the bits representing wieghts going into hidden layer 1
	while index < hiddenLayer1BitsEnd:
		weightBitString = chrom[index:index+bitsPerWeight]
		#weightList[0] accesses the data for weights going into hidden layer 1
		weightList[0][node_num][numWeightsPerCurNode] = bin2Weight(weightBitString)
		numWeightsPerCurNode +=1
		#if we are at the end of the bits of weights per this node
		if numWeightsPerCurNode == numInputs + 1:
			node_num += 1
			numWeightsPerCurNode = 0
		index += bitsPerWeight


	#Calculate/store weights from hidden layer 1 to hidden layer 2
	#Add 1 to the calculation for the side of hidden layer 2 to include the threshold
	hiddenLayer2BitsEnd = hiddenLayer1BitsEnd + numHiddenLayerNodes*(numHiddenLayerNodes + 1)*bitsPerWeight
	node_num = 0
	numWeightsPerCurNode = 0

	#While we are still looking at the bits representing wieghts going into hidden layer 2
	while index < hiddenLayer2BitsEnd:
		weightBitString = chrom[index:index+bitsPerWeight]
		#weightList[1] accesses the data for weights going into hidden layer 2
		weightList[1][node_num][numWeightsPerCurNode] = bin2Weight(weightBitString)
		numWeightsPerCurNode +=1
		#if we are at the end of the bits of weights per this node
		if numWeightsPerCurNode == numHiddenLayerNodes + 1:
			node_num += 1
			numWeightsPerCurNode = 0
		index += bitsPerWeight

	#Calculate/store weights from hidden layer 2 to the output node
	outputBitsEnd = hiddenLayer2BitsEnd + numOutputs*(numHiddenLayerNodes + 1)*bitsPerWeight
	node_num = 0
	numWeightsPerCurNode = 0

	#While we are still looking at the bits representing wieghts going into the output layer
	while index < outputBitsEnd:
		weightBitString = chrom[index:index+bitsPerWeight]
		#weightList[2] accesses the data for weights to output node
		weightList[2][node_num][numWeightsPerCurNode] = bin2Weight(weightBitString)
		numWeightsPerCurNode +=1
		if numWeightsPerCurNode == numHiddenLayerNodes + 1:
			node_num += 1
			numWeightsPerCurNode = 0

		index += bitsPerWeight

	return weightList


def initializeWeightList(numInputs, numHiddenNodes, numOutputs):
	"""Function to initialize the structure of the list of weights.
	
	Specifically, this function is called from mapChrom2Weights() so that the 
	chromsosome bit string can be translated into a list structure.

	Arguments:
		numInputs: the number of inputs in the neural network
		numHiddenNodes: the number of nodes in each of the 2 hidden layers in the neural network
		numOuputs: the number of outputs in the neural network

	Returns:
		weightStructure:  A list that serves as the structure for storing all the weights in the neural network.
		It always contains 3 lists: the first for weights between the input layer and hidden layer 1,
		the second for the weights between hdden layer 1 and hidden layer 2,
		and the third for the weights between hidden layer 2 and the output layer.
		Also, each of these 3 lists consists of lists representing all the weights going into a specific node in 
		the network.
		Note that all the weights are initialzied to 0 with this function, and are later set to
		bit strings from the mapChrom2weights() function.

	"""

	inputToHidden1Ws = []
	hidden1ToHidden2Ws = []
	hidden2ToOutputWs = []

	#Create structure for weights from input to hidden layer 1
	for i in range(numHiddenNodes): 
		#Initialize each weight connecting to hidden layer 1 node i as 0
		curInputWs = []
		for j in range(numInputs + 1): #+1 to include threshold
			curInputWs.append(0)
		inputToHidden1Ws.append(curInputWs)


	#Create structure for weights from hidden layer 1 to hidden layer 2
	for i in range(numHiddenNodes): 
		#Initialize each weight connecting to hidden layer 2 node i as 0
		curInputWs = []
		for j in range(numHiddenNodes + 1): #+1 to include threshold
			curInputWs.append(0)
		hidden1ToHidden2Ws.append(curInputWs)

	#Create structure for weights from hidden layer 2 to the output layer
	for i in range(numOutputs):
		#Initialize each weight connecting to output node i as 0
		curInputWs = []
		for j in range(numHiddenNodes + 1): #+1 to include threshold
			curInputWs.append(0)
		hidden2ToOutputWs.append(curInputWs)

	weightStructure = [inputToHidden1Ws] + [hidden1ToHidden2Ws] + [hidden2ToOutputWs]


	return weightStructure



def bin2Weight(binString):

	"""Function to covert a bit string to a weight in the neural network.
	
	Each bit is converted to a value between -3 and 3.

	Arguments:
		binString: The inputted bit string.

	Returns:
		normalized_weight: The weight to be used for the neural network.
	"""

	bitsPerWeight = len(binString)

	integer = int(binString, 2)

	#Convert integer to a value between -3 and 3

	product = 3/(2**(bitsPerWeight-1))

	normalized_weight = integer*product - 3

	return normalized_weight


def testNetwork(inputList, weightList, numHiddenLayerNodes, numOutputs):
	"""Function to calculate the final outputs in the network from the original inputs.

	Arguments:
		inputList: A list of all of the inputs into the neural network
		weightList:  A list where each element represents the weights for a layer in the network.
		It always contains 3 lists: the first for weights between the input layer and hidden layer 1,
		the second for the weights between hdden layer 1 and hidden layer 2,
		and the third for the weights between hidden layer 2 and the output layer.
		Also, each of these 3 lists consists of lists representing all the weights going into a specific node in 
		the network.
		numHiddenLayerNodes: The number of nodes for each hidden layer in the neural network.
		numOutputs: The number of outputs for the neural network.

	Returns:
		outputs: A list of all the outputs of the neural network.

	"""

	#Add -1 to be the threshold for the inputList
	inputList.append(-1)

	#Calculate output for each node in hidden layer 1
	hiddenLayer1Outputs = calcHiddenLayerOutputs(inputList, weightList[0], numHiddenLayerNodes)
	#Add threshold for next layer
	hiddenLayer1Outputs.append(-1)

	#Calculate output for each node in hidden layer 2
	hiddenLayer2Outputs = calcHiddenLayerOutputs(hiddenLayer1Outputs, weightList[1], numHiddenLayerNodes)
	#add threshold for next layer
	hiddenLayer2Outputs.append(-1)

	#Calculate output for final nodes
	finalOutputs = []
	for outputWeightList in weightList[2]:

		finalOutput = calcOutputForNeuron(hiddenLayer2Outputs, outputWeightList) 
		finalOutputs.append(finalOutput)

	return finalOutputs

def calcHiddenLayerOutputs(inputList, weightList, numHiddenLayerNodes):
	"""Function to calculate the output for each node in a specific hidden layer.

	This function is always called from testNetowrk().

	Arguments:
		inputList: A list of all inputs going into the specific hidden layer of the neural network
		weightList: A list of all the weights that going into the specific hidden layer of the
		neural network. Each element in this list is a list of all the weights going into a specific node
		of the hidden layer.
		numHiddenLayerNodes: The number of nodes for the specific hidden layer in the neural network.

	Returns:
		hiddenLayerOutputs: A list of all the outputs for each node in the specific layer based on 
		the inputs and weights.

	"""

	hiddenLayerOutputs = []

	for i in range(numHiddenLayerNodes):
		output = calcOutputForNeuron(inputList, weightList[i])
		hiddenLayerOutputs.append(output)

	return hiddenLayerOutputs


def calcOutputForNeuron(inputList, weights):
	"""Function to calculate the output for a single node/neuron in the network.

	It is called from within testNetowrk().

	Arguments:
		inputList: A list of all inputs going into the specific node of the neural network.
		weights: A list of all the weights going into the specigic node.

	Returns:
		output: The output of the single node using the sigmoid activation function.
	"""
	
	#Compute the weighted sum of inputs
	weightedSum = 0
	for j in range(len(weights)):
		inputVal = inputList[j]
		weightedSum += inputVal*weights[j]

	#Use the sigmoid function
	output = sigmoid(weightedSum)
	
	return output

def sigmoid(s):
	"""A simple sigmoid function.

	Arguments:
		s: the input into the sigmoid functon.

	Returns:
		The output from inputting s into the sigmoid function.
	"""

	return 1 / (1 + math.exp(-s))
	








