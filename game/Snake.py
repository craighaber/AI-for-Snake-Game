# **************************************************************************************
# Adapted from the work of [Craig Haber](https://github.com/craighaber) with the
# original work available at https://github.com/craighaber/AI-for-Snake-Game
# *************************************************************************************
import collections

from game.Board import Directions
from game.Coordinates import Coordinates


class Snake:
    def __init__(self, rows, cols):
        """Initializes Snake class"""

        self.rows = rows
        self.cols = cols
        self.body = []
        self.body.append(self.initialize_snake())
        self.directions = collections.deque()

    def initialize_snake(self):
        """
        Initializes the first position for the snake.

        Returns:
        A Coordinate representing the position for the snake.

        """
        snake_row = self.rows // 2
        snake_col = self.cols // 2

        return Coordinates(snake_row, snake_col)

    def update_body_positions(self):
        """
        Updates the snake's body positions.

        The snake's body positions are updated based on the directions in
        self.directions. This update occurs each frame, and is called directly
        from all the classes that run the Snake Game.
        """
        # Iterate through each square that is part of the snake's body
        for i, pos in enumerate(self.body):
            # Get the direction to move next that corresponds to the body position
            direction = self.directions[i]
            # Update the body position after moving in the direction
            self.body[i] = pos.apply_modifier(direction)

    def extend_snake(self):
        """
        Adds one extra block to the end of the snake's body.

        This function is called directly from the
        SnakeGame class whenever the snake eats a fruit.
        """
        snake_tail = self.body[-1]
        # Get the direction of the tail of the body
        tail_dir = self.directions[-1]

        # spawn the new body component in the opposite direction of the snake's movement
        match tail_dir:
            case Directions.DOWN:
                self.body.append(snake_tail.apply_modifier(Directions.UP))
            case Directions.UP:
                self.body.append(snake_tail.apply_modifier(Directions.DOWN))
            case Directions.LEFT:
                self.body.append(snake_tail.apply_modifier(Directions.RIGHT))
            case Directions.RIGHT:
                self.body.append(snake_tail.apply_modifier(Directions.LEFT))
            case _:
                raise LookupError
