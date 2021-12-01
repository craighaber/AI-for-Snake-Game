# **************************************************************************************
# Adapted from the work of [Craig Haber](https://github.com/craighaber) with the
# original work available at https://github.com/craighaber/AI-for-Snake-Game
# *************************************************************************************
import random

from game.Board import Board, States
from game.Coordinates import Coordinates
from game.Directions import Directions
from game.GameState import GameState
from game.Snake import Snake


class SnakeGame:

    def __init__(self):
        """Initializes the SnakeGame class."""
        self.rows = 10
        self.cols = self.rows
        self.snake = Snake(self.rows, self.cols)
        self.fruit_pos = Coordinates(0, 0)
        self.generate_fruit()
        self.score = 0
        self.game_state: GameState = GameState.INPROGRESS
        self.loop_around = True

    def generate_fruit(self):
        """Function to generate a new random position for the fruit."""
        fruit_pos = Coordinates(random.randrange(0, self.rows), random.randrange(0, self.cols))

        # Continually generate a location for the fruit until it is not in the snake's body
        while fruit_pos in self.snake.body:
            fruit_pos = Coordinates(random.randrange(0, self.rows), random.randrange(0, self.cols))

        self.fruit_pos = fruit_pos

    def move_snake(self, direction: Directions):
        """Function to allow the user to move the snake with the arrow keys."""

        self.snake.directions.appendleft(direction)
        if len(self.snake.directions) > len(self.snake.body):
            self.snake.directions.pop()

        self.snake.update_body_positions()

    def check_collisions(self):
        """Function that consecutively calls all the functions that detect collisions."""

        self.check_fruit_collision()
        self.check_wall_collision()
        self.check_body_collision()

    def check_fruit_collision(self):
        """Function that detects and handles if the snake has collided with a fruit."""
        # If we found a fruit
        if self.snake.body[0] == self.fruit_pos:
            # Add the new body square to the tail of the snake
            self.snake.extend_snake()
            # Generate a new fruit in a random position
            self.generate_fruit()

            self.score += 1

    def check_wall_collision(self):
        """Function that checks and handles if the snake has collided with a wall."""

        # Only need to check the collisions of the head of the snake
        head = self.snake.body[0]
        head_y = head.y_coord
        head_x = head.x_coord

        # If there is a wall collision, game over
        if head_x == self.cols or head_y == self.rows or head_x < 0 or head_y < 0:
            self.game_over()

    def check_body_collision(self):
        """Function that checks and handles if the snake has collided with its own body."""

        if len(self.snake.body) > 1:
            # Only need to check the collisions of the head of the snake
            head = self.snake.body[0]
            body_without_head = self.snake.body[1:]

            if head in body_without_head:
                self.game_over()

    def is_game_over(self):
        if self.game_state == GameState.INPROGRESS:
            return False
        else:
            return True

    def game_over(self):
        self.game_state = GameState.OVER
        return self.score

    def get_board(self):
        board = Board(self.rows, self.cols)

        for rowIndex in range(self.rows):
            for colIndex in range(self.cols):
                current_position = Coordinates(rowIndex, colIndex)
                state: States = States.NONE
                direction: Directions = Directions.NONE
                if current_position == self.fruit_pos:
                    state = States.FOOD
                    direction = Directions.NONE
                    board.set_state_at(rowIndex, colIndex, state, direction)

                elif current_position in self.snake.body:
                    state = States.SNAKE_BODY
                    head = self.snake.body[0]
                    if current_position == head:
                        state = States.SNAKE_HEAD

                    index = self.snake.body.index(current_position)
                    try:
                        direction = self.snake.directions.__getitem__(index)
                    except IndexError:
                        direction = Directions.NONE
                    board.set_state_at(rowIndex, colIndex, state, direction)

                else:
                    board.set_state_at(rowIndex, colIndex, state, direction)

        return board

    def get_score(self):
        return self.score
