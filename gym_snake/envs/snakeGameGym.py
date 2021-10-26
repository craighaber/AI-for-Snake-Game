#**************************************************************************************
#SnakeGameGym.py
#Author: Craig Haber
#5/9/2020
#Module with the SnakeGameGym class that is instantiated in testTrainedAgents.py
#to observe the best agents that were trained with the genetic algorithm.
#*************************************************************************************

import pygame
import random
import collections
import numpy as np
from gym_snake.envs.snakeGame import SnakeGame
from gym_snake.envs.snake import Snake

class SnakeGameGym(SnakeGame):
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

	def __init__(self, fps):
		"""Initializes the SnakeGameGATest class.
		
		The only agrument that is not a documented class attribute is:
			chromosome: A string of bits representing all of the weights for the neural network.
		"""

		super().__init__(fps)
	
	def get_board(self):
		"""
		Uses sefl.rows, self.cols, self.snake, and self.fruit_pos in order
		to create a list representation of the board
		0 is empty space
		1 is space with fruit in it
		2 is space with snake body in it
		3 is space with snake head
		"""
		# Initializes empty board
		board = np.zeros([self.rows, self.cols], dtype=int)

		# Add Fruit
		fruit_row = self.fruit_pos[0]
		fruit_col = self.fruit_pos[1]
		board[fruit_row][fruit_col] = 1

		# Add Snake to Board
		for i in range(len(self.snake.body)):
			body_pos = self.snake.body[i]
			
			# Add Snake Head
			if i == 0:
				board[body_pos[0]][body_pos[1]] = 3
			
			# Add Snake Body
			else:
				board[body_pos[0]][body_pos[1]] = 2

		return board

		







		return (self.snake, self.fruit_pos, self.rows)

	def move_snake(self, action):
		move_map = {
			0: "left",
			1: "up",
			2: "right",
			3: "down",
		}
		direct = move_map[action]

		self.snake.directions.appendleft(direct)
		if len(self.snake.directions) > len(self.snake.body):
			self.snake.directions.pop()

		self.snake.update_body_positions()

	def check_collisions(self):
		"""
		Function that consecutively calls all the functions that detect collisions
		Returns a reward based on these collisions

		FIXME: 
			Currently, part of checking collisions is also resetting the game
			Seems like we should disentangle these two things. First check collision, report whether collision
			occurred, and then afterwards reset the board
		"""
		fruit_collision = self.check_fruit_collision()
		wall_collision = self.check_wall_collision()
		body_collision = self.check_body_collision()		
		
		if fruit_collision:
			return 1
		elif wall_collision or body_collision:
			return -1
		else:
			return 0

	def check_fruit_collision(self):
		"""Function that detects and handles if the snake has collided with a fruit."""

		#If we found a fruit
		if self.snake.body[0] == self.fruit_pos:
			#Add the new body square to the tail of the snake
			self.snake.extend_snake()
			#Generate a new fruit in a random position
			self.generate_fruit()

			self.score += 1
			return True
		
		return False

	def check_wall_collision(self):
		"""Function that checks and handles if the snake has collided with a wall."""

		#Only need to check the colisions of the head of the snake
		head = self.snake.body[0]  # TODO: create head state variable
		head_y = head[0]
		head_x = head[1]

		#If there is a wall collision, game over
		if head_x == self.cols or head_y == self.rows or head_x < 0 or head_y < 0:
			self.game_over()
			return True
		
		return False

	def check_body_collision(self):
		"""Function that checks and handles if the snake has collided with its own body."""

		if len(self.snake.body) > 1:
			#Only need to check the colisions of the head of the snake
			head = self.snake.body[0]
			body_without_head = self.snake.body[1:]

			if head in body_without_head:
				self.game_over()
				return True

		return False



