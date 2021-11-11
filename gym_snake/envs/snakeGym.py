
import collections
import random
from gym_snake.envs.snake import Snake

class SnakeGym(Snake):

	"""Class that represents the snake in Snake Game.

	It is instatiated from within the SnakeGame class

	Attributes:
		self.rows: The number of rows in the grid of the game
		self.cols: The number of columns in the grid of the game
		self.body: A list of positions in the grid of the Snake's body
		self.directions: A double-ended queue corresponding to self.body,
		representing each direction each body part will move next.
	"""

	def __init__(self,rows,cols,start_snake_pos):
		"""Initializes Snake class"""

		self.rows = rows
		self.cols = cols
		self.body = []
		self.body.append(start_snake_pos)
		self.directions = collections.deque()
