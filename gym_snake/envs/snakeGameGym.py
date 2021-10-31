#**************************************************************************************
#snakeGameGym.py
#Module with the SnakeGameGym class that is instantiated in testTrainedAgents.py
#to observe the best agents that were trained with the reinforcement learning algorithm.
#*************************************************************************************

import numpy as np
from gym import spaces
from gym_snake.envs.snakeGame import SnakeGame
from gym_snake.envs.snake import Snake

class SnakeGameGym(SnakeGame):
	"""
	Class framework to observe agents who were trained with the reinforcement algortihm to play the Snake Game.

	Inherits the SankeGame class that runs the Snake Game.
	"""

	def __init__(self, fps: int):
		"""
		Initializes the SnakeGameGATest class.
		"""
		self.move_map = {
			0: "left",
			1: "up",
			2: "right",
			3: "down",
		}

		super().__init__(fps)
	
	def pos_on_board(self, pos):
		# If row index is less than 0 or greater than number of rows, pos is not on board
		if pos[0] < 0 or pos[0] >= self.rows:
			return False

		# If col index is less than 0 or greater than number of cols, pos is not on board
		if pos[1] < 0 or pos[1] >= self.cols:
			return False		

		# Otherwise, pos is on board
		return True

	def get_board(self) -> np.ndarray:
		"""
		Uses sefl.rows, self.cols, self.snake, and self.fruit_pos in order
		to create a list representation of the board
		0 is empty space
		1 is space with fruit in it
		2 is space with snake body in it
		3 is space with snake head in it
		"""
		# Initializes empty board
		board = np.zeros([self.rows, self.cols], dtype=int)

		# Add Fruit
		fruit_row = self.fruit_pos[0]
		fruit_col = self.fruit_pos[1]
		board[fruit_row][fruit_col] = 1

		# Add Snake to Board
		for i in range(len(self.snake.body)):
			pos = self.snake.body[i]
			
			# If body position is outside of the board, do not add this to board representation
			if not self.pos_on_board(pos):
				# FIXME: figure out a better way to represent this condition
				pass

			# Add Snake Head
			elif i == 0:
				board[pos[0]][pos[1]] = 3
			
			# Add rest of Snake Body
			else:
				board[pos[0]][pos[1]] = 2

		return board

	def move_snake(self, action: spaces.Discrete(4)) -> None:
		"""
		Function that moves the snake on the board in one of four possible directions
		using a discrete 4-item action space as input.
		"""
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

	def check_collisions(self) -> int:
		"""
		Function that consecutively calls all the functions that detect collisions
		Returns a reward based on these collisions
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
