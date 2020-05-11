#**************************************************************************************
#snakeGameGATrain.py
#Author: Craig Haber
#5/9/2020
#Module with the SnakeGameGATrain class that is instantiated in testGenticAlgorithm.py
#to train a population of intelligent Sanke Game agents.
#*************************************************************************************

import pygame
import random
import collections
from helpers.snakeGameGATest import SnakeGameGATest
from helpers.snake import Snake
from helpers import neuralNetwork as nn
from helpers import geneticAlgorithm as ga 
import os


class SnakeGameGATrain(SnakeGameGATest):
	"""Class framework to train a population of intelligent Snake Game agents through a genetic algorithm.

	This class inherets from the SnakeGameGATest class (since the two classes are quite similar), which
	inherets from the SnakeGame class.
	The actual methods if the genetic algorithm are in geneticAlgorithm.py.

	Attributes:
		self.cur_chrom: An index of the current chromosome being tested in self.population.
		self.frames_alive: The number of frames the current agent has been alive, used for the fitness function.
		self.chroms_per_gen: The number of chromosomes in a generation (equivalent to the population size).
		self.population: A list of all the chromosomes in the population for the current generation.
		self.weights: The weights for the neural network converted from the current chromosome.
		self.fitness_scores: A list of all the fitness scores, each index corresponding to a chromosome in self.population.
		self.game_scores: A list of all the in-game scores, each index corresponding to a chromosome in self.population.
		self.num_generation: The number of generations that have passed.
	"""

	def __init__(self, fps, population, chroms_per_gen, bits_per_weight, num_inputs, num_hidden_layer_nodes, num_outputs):
		"""Initializes the SnakeGameGATrain class

		Arguments:
			fps: The frame rate of the game.
			population: A list of all the chromosomes in the population for the current generation.
			chroms_per_gen: The number of chromosomes in a generation (equivalent to the population size).
			bits_per_weight: The number of bits per each weight in the nueral network.
			num_inputs: The number of inputs in the neural network.
			num_hidden_layer_nodes: The number of nodes per each of the 2 hidden layers in the neural network.
			num_ouputs: The number of outputs in the neural network.
		"""
		
		super().__init__(fps, "", bits_per_weight, num_inputs, num_hidden_layer_nodes, num_outputs)
		self.cur_chrom = 0
		self.frames_alive = 0
		self.chroms_per_gen = chroms_per_gen
		self.population = population
		self.weights = nn.mapChrom2Weights(self.population[self.cur_chrom], self.bits_per_weight, self.num_inputs, self.num_hidden_layer_nodes, self.num_outputs)
		self.fitness_scores = []
		self.game_scores = []
		self.num_generations = 0


	def game_over(self):
		"""Function that restarts the game upon game over.

		This overrides the method in the SnakeGameGATest superclass."""

		#Make necessary updates to move onto the next chromosome.
		self.fitness_scores.append(self.calc_fitness())
		self.cur_chrom +=1
		self.game_scores.append(self.score)

		#If we are done testing all the chromsomes in the population.
		if self.cur_chrom == self.chroms_per_gen:
			#Move onto next generation
			self.num_generations +=1
			next_generation, best_individual, best_fitness, average_fitness = ga.createNextGeneration(self.population, self.fitness_scores)
			
			self.population = next_generation
			self.cur_chrom  = 0
			self.fitness_scores = []

			average_game_score = sum(self.game_scores)/len(self.game_scores)

			high_score_per_cur_gen = max(self.game_scores)

			print(self.num_generations, self.high_score, average_game_score, high_score_per_cur_gen, average_fitness)

			self.game_scores = []

			#Write data about this generation to ga_data.txt
			file = open("GAdata.txt", "a+")
			file.write("Generation " + str(self.num_generations) + "\n")
			file.write("Best Individual: " + str(best_individual) + "\n")
			file.write("Best Fitness: " + str(best_fitness) + "\n")
			file.write("Average Fitness:" + str(average_fitness) + "\n")
			file.write("Average Game Score:" + str(average_game_score) + "\n\n")
			file.write("\n")
			file.close()

			#Every 10 generations save the population to a file in the populations folder
			if self.num_generations%10 == 0:
				#Get the path of the directory with all the populations
				abs_file_path = os.path.join(os.getcwd(), "populations/population_" + str(self.num_generations) + ".txt")
				file = open(abs_file_path, "a+")
				file.write(str(self.population))
				file.write("\n")
				file.close()

		self.weights = nn.mapChrom2Weights(self.population[self.cur_chrom], self.bits_per_weight, self.num_inputs, self.num_hidden_layer_nodes, self.num_outputs)

		#Reset the game itself
		self.snake = Snake(self.rows,self.cols)
		self.generate_fruit()
		self.restart = True
		if self.score > self.high_score:
			self.high_score = self.score
		self.score = 0
		self.frames_alive = 0
		self.frames_since_last_fruit = 0

	def calc_fitness(self):
		"""Function to calculate the fitness score for a chromosome.
		
		Returns: A fitness score.
		"""

		frame_score = self.frames_alive
		#If the frames since the last fruit was eaten is at least 50
		if self.frames_since_last_fruit >= 50:
			#Subtract the number of frames since the last fruit was eaten from the fitness
			#This is to discourage snakes from trying to gain fitness by avoiding fruit
			frame_score = self.frames_alive - self.frames_since_last_fruit
			#Ensure we do not multiply fitness by a factor of 0
			if frame_score <= 0:
					frame_score = 1

		return ((self.score*2)**2)*(frame_score**1.5)