#**************************************************************************************
#snakeGameGym.py
#Module with the SnakeGameGym class that is instantiated in testTrainedAgents.py
#to observe the best agents that were trained with the reinforcement learning algorithm.
#*************************************************************************************

import random
import numpy as np
from gym import spaces
from gym_snake.envs.snakeGame import SnakeGame
from gym_snake.envs.snakeGym import SnakeGym
import pygame


class SnakeGameGym(SnakeGame):
	"""
	Class framework to observe agents who were trained with the reinforcement algortihm to play the Snake Game.

	Inherits the SankeGame class that runs the Snake Game.
	"""

	def __init__(self,
		board_height: int, 
		board_width:int, 
		max_moves_no_fruit: int,
		use_pygame: bool):
		"""
		Initializes the SnakeGameGym class.

		board_height: the number of rows on the game board.
		board_width: the number of columns on the game board.
		max_moves_no_fruit: number of allowed consecutive moves that do not result in fruit consumption. 
									   Non-positive values correspond to no limit.
		use_pygame: boolean flag for whether or not to visualize the environment with pygame.
		"""
		# SnakeGameGym specific instance variables
		self.use_pygame = use_pygame
		self.move_map = {
			0: "left",
			1: "up",
			2: "right",
			3: "down",
		}
		self.max_moves_no_fruit = max_moves_no_fruit
		self.num_moves_since_fruit = 0
		
		# original Snake instance variables
		self.width = 500
		self.height = 600
		self.grid_start_y = 100
		self.play = True
		self.restart = False
		self.rows = board_height
		self.cols = board_width
		self.snake = SnakeGym(self.rows, self.cols, self.get_rand_pos())
		self.fruit_pos = (0,0)
		self.generate_fruit()
		self.score = 0
		self.high_score = 0
		self.last_head_pos = self.snake.body[0]

		# initializing pygame visualization
		if self.use_pygame:
			self.win = pygame.display.set_mode((self.width, self.height))
			self.clock = pygame.time.Clock()

	def get_rand_pos(self):
		"""
		Function that returns a random position on the board.
		"""
		rand_row = random.randrange(0, self.rows)
		rand_col = random.randrange(0, self.cols)

		return (rand_row, rand_col)

	def pos_on_board(self, pos):
		"""
		Function that checks if a given position is on the board.
		"""
		# If row index is less than 0 or greater than number of rows, pos is not on board
		if pos[0] < 0 or pos[0] >= self.rows:
			return False

		# If col index is less than 0 or greater than number of cols, pos is not on board
		if pos[1] < 0 or pos[1] >= self.cols:
			return False		

		# Otherwise, pos is on board
		return True

	def get_board(self, represent_border=False) -> np.ndarray:
		"""
		Args:
			represent_border: bool flag for whether to represent the border in the board.
		Uses sefl.rows, self.cols, self.snake, and self.fruit_pos in order
		to create a list representation of the board
		-1 is border (if applicable)
		0 is empty space
		1 is space with fruit in it
		2 is space with snake body in it
		3 is space with snake head in it
		"""
		# Initializes empty board
		board = np.zeros([self.rows, self.cols], dtype=int)
		border_space = 0

		if represent_border:
			board = np.zeros([self.rows+2, self.cols+2], dtype=int)
			border_space = 1  # FIXME: can be replaced with int(represent_border)

			# Create border of -1
			board[0] = -1
			board[-1] = -1
			for r in range(board.shape[0]):
				board[r][0] = -1
				board[r][-1] = -1

		# Add Fruit
		fruit_row = self.fruit_pos[0] + border_space
		fruit_col = self.fruit_pos[1] + border_space
		board[fruit_row][fruit_col] = 1

		# Add Snake to Board
		for i in range(len(self.snake.body)):
			pos = self.snake.body[i]
			snake_row = pos[0] + border_space
			snake_col = pos[1] + border_space
			
			# If body position is outside of the board, do not add this to board representation
			# This is not needed if we represent the border
			if not represent_border and not self.pos_on_board(pos):
				pass

			# Add Snake Head
			elif i == 0:
				board[snake_row][snake_col] = 3
			
			# Add rest of Snake Body
			else:
				board[snake_row][snake_col] = 2

		return board

	def move_snake(self, action: spaces.Discrete(4)) -> None:
		"""
		Function that moves the snake on the board in one of four possible directions
		using a discrete 4-item action space as input.
		"""
		self.last_head_pos = self.snake.body[0]

		direct = self.move_map[action]

		self.snake.directions.appendleft(direct)
		if len(self.snake.directions) > len(self.snake.body):
			self.snake.directions.pop()

		self.snake.update_body_positions()

	def respond_to_fruit_consumption(self) -> int:
		"""
		Function that extends a snake, generates new snake tail block and fruit,
		and updates/returns the new score
		"""
		#Add the new body square to the tail of the snake
		self.snake.extend_snake()
		#Generate a new fruit in a random position
		self.generate_fruit()
		#Update score
		self.score += 1

		return self.score

	def check_fruit_collision(self) -> bool:
		"""
		Function that detects and handles if the snake has collided with a fruit.
		"""
		#If we found a fruit
		if self.snake.body[0] == self.fruit_pos:
			return True
		
		return False

	def check_wall_collision(self) -> bool:
		"""
		Function that checks and handles if the snake has collided with a wall.
		"""
		#Only need to check the colisions of the head of the snake
		head = self.snake.body[0]  # TODO: create head state variable
		head_y = head[0]
		head_x = head[1]

		#If there is a wall collision, game over
		if head_x == self.cols or head_y == self.rows or head_x < 0 or head_y < 0:
			return True
		
		return False

	def check_body_collision(self) -> bool:
		"""
		Function that checks and handles if the snake has collided with its own body.
		"""
		if len(self.snake.body) > 1:
			#Only need to check the colisions of the head of the snake
			head = self.snake.body[0]
			body_without_head = self.snake.body[1:]

			#Check for head collision with rest of snake body
			if head in body_without_head:
				return True

		return False

	def check_exceeded_max_moves(self) -> bool:
		"""
		Function that checks whether or not the snake has made too many moves since 
		last consuming a fruit.
		"""
		return (self.max_moves_no_fruit > 0 and # non-positive max move count default returns false
				not self.check_fruit_collision() and # if the snake's head is in the same space as a fruit return false
				self.num_moves_since_fruit > self.max_moves_no_fruit) #

	def reset_moves_since_fruit(self) -> None:
		"""
		Helper function for resetting num_current_moves_since_fruit
		"""
		self.num_moves_since_fruit = 0

	def increment_moves_since_fruit(self) -> None:
		"""
		Helper function for incrementing num_current_moves_since_fruit
		"""
		self.num_moves_since_fruit += 1
		
	def check_closer_to_fruit(self) -> bool:
		"""
		Function that checks if the snake has moved closer to the fruit.
		"""
		head = self.snake.body[0]
		return self.manhattan_distance(self.fruit_pos,self.last_head_pos) > self.manhattan_distance(self.fruit_pos, head)

	def manhattan_distance(self, pos1, pos2) -> bool:
		"""
		Function that returns simple city-block distance
		"""
		row_diff = abs(pos1[0] - pos2[0])
		col_diff = abs(pos1[1] - pos2[1])

		return row_diff + col_diff

	def game_over(self):
		"""Function that restarts the game upon game over."""

		self.snake = SnakeGym(self.rows,self.cols, self.get_rand_pos())
		self.generate_fruit()
		if(self.score > self.high_score):
			self.high_score = self.score
		self.restart = True
		self.score = 0
