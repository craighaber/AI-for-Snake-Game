#*********************************************************************************
#snake.py
#Author: Craig Haber
#5/9/2020
#This module contains the Snake class, which is used to run the Snake Game.
#*********************************************************************************

import collections

class Snake():

	"""Class that represents the snake in Snake Game.

	It is instatiated from within the SnakeGame class

	Attributes:
		self.rows: The number of rows in the grid of the game
		self.cols: The number of columns in the grid of the game
		self.body: A list of poisitions in the grid of the Snake's body
		self.directions: A double-ended queue corresponding to self.body,
		representing each direction each body part will move next.
	"""

	def __init__(self,rows,cols):
		"""Initializes Snake class"""

		self.rows = rows
		self.cols = cols
		self.body = []
		self.body.append(self.initialize_snake())
		self.directions = collections.deque()

	def initialize_snake(self):
		"""Initializes the first position for the snake.

		Returns:
			A tuple representing the position for the snake in
			the format of (row, column).

		"""
		snake_row = self.rows//2
		snake_col = 1

		return (snake_row,snake_col)

	def update_body_positions(self):
		"""Updates the snake's body positions.

		The snake's body positions are updated based on the directions in
		self.directions. This update occurs each frame, and is called directly
		from all the classes that run the Snake Game.
		"""
		#Iterate through each square that is part of the snake's body
		for i,pos in enumerate(self.body):
			#Get the direction to move next that corresponds to the body position
			direct = self.directions[i]
			#Update the body position after moving in the direction
			if direct == "left":
				#Move left
				self.body[i] = (pos[0],pos[1]-1)		
			elif direct == "up":
				#Move up
				self.body[i] = (pos[0]-1,pos[1])
			
			elif direct == "right":
				#Move right
				self.body[i] = (pos[0],pos[1]+1)		
			else:
				#Move down
				self.body[i] = (pos[0]+1, pos[1])


	def extend_snake(self):
		"""Adds one extra block to the end of the snake's body.

		This function is called directly from the
		SankeGame class whenever the snake eats a fruit."""

		snake_tail = self.body[-1]
		#Get the direction of the tail of the body
		tail_dir = self.directions[-1]

		if tail_dir == "left":
			#If tail is going left, add new tail to right of old tail
			self.body.append((snake_tail[0], snake_tail[1]+1))
		elif tail_dir == "up":
			#If tail is going up, add new tail below old tail
			self.body.append((snake_tail[0]+1, snake_tail[1]))
		elif tail_dir == "right":
			#If tail is going right, add new tail to the left of old tail
			self.body.append((snake_tail[0], snake_tail[1]-1))
		else:
			#If tail is going down, add new tail above old tail
			self.body.append((snake_tail[0]-1, snake_tail[1]))
