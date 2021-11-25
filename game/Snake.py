# **************************************************************************************
# Adapted from the work of [Craig Haber](https://github.com/craighaber) with the
# original work available at https://github.com/craighaber/AI-for-Snake-Game
# *************************************************************************************
import collections

from game.Board import Directions


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
        A tuple representing the position for the snake in
        the format of (row, column).

        """
        snake_row = self.rows // 2
        snake_col = self.cols // 2

        return snake_row, snake_col

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
            if direction == Directions.LEFT:
                # Move left
                self.body[i] = (pos[0], pos[1] - 1)
            elif direction == Directions.UP:
                # Move up
                self.body[i] = (pos[0] - 1, pos[1])

            elif direction == Directions.RIGHT:
                # Move right
                self.body[i] = (pos[0], pos[1] + 1)
            elif direction == Directions.DOWN:
                # Move down
                self.body[i] = (pos[0] + 1, pos[1])
            else:
                raise LookupError

    def extend_snake(self):
        """
        Adds one extra block to the end of the snake's body.

        This function is called directly from the
        SnakeGame class whenever the snake eats a fruit.
        """
        snake_tail = self.body[-1]
        # Get the direction of the tail of the body
        tail_dir = self.directions[-1]

        if tail_dir == Directions.LEFT:
            # If tail is going left, add new tail to right of old tail
            self.body.append((snake_tail[0], snake_tail[1] + 1))
        elif tail_dir == Directions.UP:
            # If tail is going up, add new tail below old tail
            self.body.append((snake_tail[0] + 1, snake_tail[1]))
        elif tail_dir == Directions.RIGHT:
            # If tail is going right, add new tail to the left of old tail
            self.body.append((snake_tail[0], snake_tail[1] - 1))
        elif tail_dir == Directions.DOWN:
            # If tail is going down, add new tail above old tail
            self.body.append((snake_tail[0] - 1, snake_tail[1]))
        else:
            raise LookupError
