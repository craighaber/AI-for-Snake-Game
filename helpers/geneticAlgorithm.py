#*********************************************************************************
#geneticAlgorithm.py
#Author: Craig Haber
#5/9/2020
#This module contains functions for a genetic algorithm made entirely from scratch.
#It uses Single-point crossover and an (n+n method) referenced in the paper
#"Snake game AI: Movement rating functions and evolutionary algorithm-based optimization"
#DOI: 10.13140/RG.2.2.33593.36969
#The functions are utilized in snakeGameGATrain.py.
#*********************************************************************************

import random
import itertools
import statistics

def genPopulation(popSize, numBits):
	"""Function that randomly generates a population of chromosomes

	Arguments:
		popSize: The number of indivduals/chromosomes in the population.
		numBits: The number of bits per each chromosome.

	Returns:
		chromosomes: A list of all the chromosome bit strings in the population.
	"""

	chromosomes = []

	for _ in range(popSize):

		chromosome = ""

		for _ in range(numBits):

			bit = random.randrange(2)
			chromosome += str(bit)

		chromosomes.append(chromosome)

	return chromosomes

def createNextGeneration(parentPop, fitnessScores):
	"""Function that moves onto the next generation by employing selection, crossover, and mutation on a population

	Arguments:
		parentPop: A list of chromosome bit strings representing the parent population.
		fitnessScores: A list of fitness scores that corresponds to each chromosome in parentPop by index.

	Returns:
		childPop: The new population of chromosome bit strings.
		bestIndividual: The chromsome with the highest fitness from the parent population.
		bestFitness: The highest fitness from the parent population.
		averageFitness: The average fitness score of the parent population.
	"""

	#Assign fitness scores
	fitnessRouletteCutoffs, bestIndividual, bestFitness, averageFitness = assignFitnessRatios(parentPop, fitnessScores)

	childPop = []

	#Save the best individuals from the previous generation
	bestParents  = extractBestParents(parentPop, fitnessScores)

	#Create a child population the same size as the parent population
	for _ in range(len(parentPop) - len(bestParents)):

		#Selection
		selectedPair = selection(parentPop, fitnessRouletteCutoffs)
		#Crossover
		child = crossOver(selectedPair)
		#Mutation
		child = mutation(child)

		childPop.append(child)

	#Combine the best parents from the old generation with the new generation
	childPop = childPop + bestParents

	return childPop, bestIndividual, bestFitness, averageFitness


def assignFitnessRatios(parentPop, fitnessScores):

	"""Function that converts each fitness score to a ratio and outputs stats the fitness of a population.
	
	Arguments:
		parentPop: A list of chromosome bit strings representing the parent population.
		fitnessScores: A list of fitness scores that corresponds to each chromosome in parentPop by index.

	Returns:
		fitnessRouletteCutoffs: A list of increasing decimal values between 0 and 1 and ending at 1, which
		are used to assign a proability of selection.
		bestIndividual: The chromsome with the highest fitness from the parent population.
		bestFitness: The highest fitness from the parent population.
		averageFitness: The average fitness score of the parent population.
	"""

	#Get data about the fitness scores
	bestFitness = max(fitnessScores)
	bestIndividual = parentPop[fitnessScores.index(bestFitness)]
	totalScore = sum(fitnessScores)
	averageFitness = totalScore/len(fitnessScores)
	

	#Calculate the fitness ratios
	#Each score in the list of fitness ratios corresponds to
	#the chromosome in the parentPop list at the same index
	fitnessRatios = []

	totalScore = sum(fitnessScores)
	#Calculate the fitness ratios
	for score in fitnessScores:
		ratio = score/totalScore
		fitnessRatios.append(ratio)

	#Get the cutoffs for roulette wheel selection
	#each cutoff corresponds to the chromosome in the parentPop list at the same index
	fitnessRouletteCutoffs = list(itertools.accumulate(fitnessRatios))

	return fitnessRouletteCutoffs, bestIndividual, bestFitness, averageFitness


def extractBestParents(parentPop, fitnessScores):
	"""Function that extracts the parent chromosomes with a fitness in the top 1/2 of scores.
	
	This is known as the (n+n) method, and is used to save parent chromosomes in case they are valuable.

	Arguments:
		parentPop: A list of chromosome bit strings representing the parent population.
		fitnessScores: A list of fitness scores that corresponds to each chromosome in parentPop by index.
	Returns:
		bestParents: A list of the chromsome bit strings with the top 1/2 of fitness scores.

	"""

	fitnessScoresCopy = fitnessScores.copy()
	fitnessScoresCopy.sort()

	maxIndex = len(fitnessScores) - 1

	bestScoresCutoffIndex = int(maxIndex*(1/2))

	#Get a cutoff value for the median fitness score
	bestScoresCutoff = fitnessScoresCopy[bestScoresCutoffIndex]

	bestParents = []

	#Find the chromsomes with fitness scores above the cutoff
	for i in range(len(parentPop)):

		if fitnessScores[i] > bestScoresCutoff:
			bestParents.append(parentPop[i])

	return bestParents




def selection(parentPop, fitnessRouletteCutoffs):
	"""Function to do selection for the genetic algorithm to get one pair of parent chromosome bit strings.

	Arguments:
		parentPop: A list of chromosome bit strings representing the parent population.
		fitnessRouletteCutoffs: A list of increasing decimal values between 0 and 1 and ending at 1, which
		are used to assign a proability of selection.
	Returns:
		pair: A list of the two selected parent chromsome bit strings.
	"""

	pair = []
	
	#Select two individuals randomly from the parent population to mate
	for _ in range(2):

		#Get a random value between 0 and 1
		randVal = random.random()

		for i, cutoff in enumerate(fitnessRouletteCutoffs):
			#If the random value is less than the cutoff, then select the 
			#chromosome in the parent population with the corresponding index
			if randVal < cutoff:
				pair.append(parentPop[i])
				break

	return pair

def crossOver(pair):
	"""Function to do Single-point crossover for a pair of parent chromosomes.
	
	Crossover creates one child chromsosome from two parent chromsomes by
	dividing up the bits of each parent.

	Attributes:
		pair: A pair of parent chromsome bit strings.
	Returns:
		child: The child chromosome bit string created from the pair of parent chromosomes.
	"""


	#Randomly determine which chromosome that is crossed over at the first
	#half and which is cross over at the second half

	randVal = random.randrange(2)
	startWithFirst = True
	if randVal == 0:
		startWithFirst = False

	#Randomly determine the crossover point
	#Start by getting the number of bits in an individual chromosome
	numBits = len(pair[0])
	crossOverPoint = random.randrange(numBits)

	#Create child offpsring with crossover
	child = ""
	if startWithFirst:
		#If the crossoverpoint is past the final bit, no need for concatenation
		if crossOverPoint == numBits - 1:
			child = pair[1]
		else:
			child = pair[0][:crossOverPoint] + pair[1][crossOverPoint:]
	else:
		#If the crossoverpoint is past the final bit, no need for concatenation
		if crossOverPoint == numBits - 1:
			child = pair[0]
		else:
			child = pair[1][:crossOverPoint] + pair[0][crossOverPoint:]

	return child

def mutation(chrom):
	"""Function for mutation on a single chromosome

	The mutation rate is .008.

	Attributes:
		chrom: The chromosome bit string to be potentially mutated
	Returns:
		newString: The potentially mutated chromosome bit string
	"""

	#Probability each bit is mutated
	MUTATION_RATE = .008
	#Convert the chromsome bit string into a list
	bitList = list(chrom)
	for i,bit in enumerate(bitList):

		randVal = random.random()

		#If the random chance of mutation occured
		if randVal < MUTATION_RATE:
			#Flip the bit
			if bitList[i] == "0":
				bitList[i] = "1"
			else:
				bitList[i] = "0"

	newString = "".join(bitList)

	return newString



