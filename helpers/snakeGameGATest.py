#**************************************************************************************
#snakeGameGATest.py
#Author: Craig Haber
#5/9/2020
#Module with the SnakeGameGATest class that is instantiated in testTrainedAgents.py
#to observe the best agents that were trained with the genetic algorithm.
#*************************************************************************************

import pygame
import random
import collections
from gym_snake.envs.snakeGame import SnakeGame
from gym_snake.envs.snake import Snake
from helpers import neuralNetwork as nn

class SnakeGameGATest(SnakeGame):
	"""Class framework to observe agents who were trained with the genetic algortihm to play the Snake Game.

	Inherits the SankeGame class that runs the Snake Game.

	Attributes:
		self.frames_since_ladt_fruit: The number of frames since the last fruit was eaten by a snake.
		self.bits_per_weight: The number of bits per each weight in the nueral network.
		self.num_inputs: The number of inputs in the neural network.
		self.num_hidden_layer_nodes: The number of nodes per each of the 2 hidden layers in the neural network.
		self.num_ouputs: The number of outputs in the neural network.
		self.weights: The weights for the neural network converted from the chromosome bit sequence of the agent.
	"""

	def __init__(self, fps, chromosome, bits_per_weight, num_inputs, num_hidden_layer_nodes, num_outputs):
		"""Initializes the SnakeGameGATest class.
		
		The only agrument that is not a documented class attribute is:
			chromosome: A string of bits representing all of the weights for the neural network.
		"""

		super().__init__(fps)
		self.frames_since_last_fruit = 0
		self.bits_per_weight = bits_per_weight
		self.num_inputs = num_inputs
		self.num_hidden_layer_nodes = num_hidden_layer_nodes
		self.num_outputs = num_outputs
		#chromsome will be an empty string if this class was inhereted from the class SnakeGameGATrain
		#This is because there will be a population of chromosomes, and not just one chromosome to test
		if chromosome != "":
			self.weights = nn.mapChrom2Weights(chromosome, self.bits_per_weight, self.num_inputs, self.num_hidden_layer_nodes, self.num_outputs)
	
	
	def move_snake(self):
		"""Function that determines where snake should move next based on the nueral network.

		This overrides the method in the SnakeGame superclass.
		"""
		
		head = self.snake.body[0]

		#Get the manhattan ditance of the fruit from the head if it moves in each direction
		dist_left_fruit = self.manhattan_distance(head[0],head[1]-1)
		dist_up_fruit = self.manhattan_distance(head[0]-1,head[1])
		dist_right_fruit = self.manhattan_distance(head[0],head[1]+1)
		dist_down_fruit = self.manhattan_distance(head[0]+1, head[1])

		#Calculate the space available for turning in each of the four directions, reduced by a constant factor
		constant = 20
		open_spaces_left = self.calc_open_spaces((head[0], head[1]-1))/constant
		open_spaces_up = self.calc_open_spaces((head[0]-1, head[1]))/constant
		open_spaces_right = self.calc_open_spaces((head[0], head[1]+1))/constant
		open_spaces_down = self.calc_open_spaces((head[0]+1, head[1]))/constant

		#Get the length of the snake
		length = self.score + 1
	
		network_inputs = [dist_left_fruit, dist_up_fruit, dist_right_fruit, dist_down_fruit,  open_spaces_left, open_spaces_up, open_spaces_down, open_spaces_right, length]

		#Get all of the outputs from the neural network indicating a value of "goodness" for turning in each direction
		outputs = nn.testNetwork(network_inputs, self.weights, self.num_hidden_layer_nodes, self.num_outputs)
		#Get the maximum of all the ouputs, and this is the direction to turn
		max_output = max(outputs)
		#Systematically decide which direction to turn based on the max output
		if max_output == outputs[0]:
			direct = "left"
		elif max_output == outputs[1]:
			direct = "up"
		elif max_output == outputs[2]:
			direct = "right"
		else:
			direct = "down"

		self.snake.directions.appendleft(direct)
		if len(self.snake.directions) > len(self.snake.body):
			self.snake.directions.pop()

		self.snake.update_body_positions()

	def manhattan_distance(self, y_head, x_head):
		"""Function to calculate the manhattan distance between the fruit and the snake's head

		Arguments:
			y_head: The row in the grid of the snake's head.
			x_head: The column in the grid of the snake's head.

		Returns:
			The manhattan distance between the fruit and the snake's head.
		"""
		return abs(self.fruit_pos[0] - y_head) + abs(self.fruit_pos[1] - x_head)

	def calc_open_spaces(self,start_pos):
		"""Function to calculate the number of open spaces around the snake 

		An open space is a space that the snake can reach without being blocked off by
		the wall or its own body.

		Arguments:
			start_poistion: A tuple in (row,column) format representing a position of the snake's head

		Returns:
			An integer of how many open spaces are available.
		"""
		open_spaces = 0

		start_y = start_pos[1]
		start_x = start_pos[0]

		#If the start position is in the snake's body or out of bounds
		if start_pos in self.snake.body or (start_x < 0 or start_x >= self.cols or start_y < 0 or start_y >= self.rows):
				#no open spaces
				return 0

		#Breadth first search is used

		#Create a set to represent th visited spaces
		visited = set([start_pos])
		#Create a queue to keep track of which spaces need to be expanded
		queue = collections.deque([start_pos])

		#While there are still unvisited open spaces to search from
		while len(queue) > 0:

			cur = queue.popleft()

			possible_moves = self.get_possible_moves(cur)

			for move in possible_moves:
				if move not in visited:

					visited.add(move)

					#if the move is an open space
					if move not in self.snake.body:
						open_spaces +=1
						#add the open space to the queue for further searching
						queue.append(move)

		return open_spaces

	def get_possible_moves(self,cur):
		"""Function to get all the possible adjacent moves from a position.

		The function is called from calc_open_spaces() during the breadth first search.

		Arguments:
			cur: A tuple in (row,column) format representing the position
			to get the next possible moves from.

		Returns:
			A list containing (row,column) tuples of all the possible adjacent moves.
		"""

		adjacent_spaces = [(cur[0], cur[1]-1), (cur[0]-1,cur[1]), (cur[0], cur[1]+1), (cur[0]+1, cur[1])]
		possible_moves = []
		for move in adjacent_spaces:
			move_y = move[1]
			move_x = move[0]
			#If the move is not out of bounds
			if move_x >= 0 and move_x < self.cols and move_y >= 0 and move_y < self.rows:
					possible_moves.append(move)
		return possible_moves


	def check_fruit_collision(self):
		"""Function that detects and handles if the snake has collided with a fruit.

		This overrides the method in the SnakeGame superclass."""

		#If we found a fruit
		if self.snake.body[0] == self.fruit_pos:
			#Add the new body square to the tail of the snake
			self.snake.extend_snake()
			#Generate a new fruit in a random position
			self.generate_fruit()

			self.score += 1
			self.frames_since_last_fruit = 0


	def update_frames_since_last_fruit(self):
		"""Function to check if the snake needs to be killed for not eating a fruit in a while."""
		
		self.frames_since_last_fruit += 1
		if (self.frames_since_last_fruit == 50 and self.score < 6) or self.frames_since_last_fruit == 250:
			self.game_over()

	
	def game_over(self):
		"""Function that restarts the game upon game over.

		This overrides the method in the SnakeGame superclass."""

		self.snake = Snake(self.rows,self.cols)
		self.generate_fruit()
		self.restart = True
		if self.score > self.high_score:
			self.high_score = self.score
		self.score = 0
		self.frames_since_last_fruit = 0




